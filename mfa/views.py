from .models import Client, EmailOTP
from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta
import hashlib
import random
from .models import Client
from django.utils import timezone
from io import BytesIO
import qrcode
import pyotp
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client, TOTPDevice
from rest_framework.permissions import BasePermission
from developers.models import DeveloperApp


class AppSecretKeyPermission(BasePermission):
    """
    Only allow access if valid X-App-Secret header is provided
    """

    def has_permission(self, request, view):
        app_secret = request.headers.get("X-App-Secret")
        if not app_secret:
            return False
        try:
            developer_app = DeveloperApp.objects.get(app_secret_key=app_secret)
            request.developer_app = developer_app  # attach app for view
            return True
        except DeveloperApp.DoesNotExist:
            return False


class TOTPSetupView(APIView):
    permission_classes = [AppSecretKeyPermission]

    def post(self, request):
        developer_app = request.developer_app
        external_user_id = request.data.get("external_user_id")
        if not external_user_id:
            return Response({"error": " external_user_id is required "}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get client
        client, created = Client.objects.get_or_create(
            developer_app=developer_app,
            external_user_id=external_user_id,
            defaults={"mfa_type": "totp", "is_active": True},
        )

        # Create TOTP device if not exists
        if not hasattr(client, "totp_device"):
            secret = pyotp.random_base32()
            totp_device = TOTPDevice.objects.create(
                client=client, secret_key=secret)
        else:
            totp_device = client.totp_device
            secret = totp_device.secret_key

        # Generate otpauth URI
        otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(
            name=str(external_user_id),
            issuer_name=developer_app.app_name
        )

        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(otpauth_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert image to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return Response({
            "success": True,
            "secret_key": secret,
            "qr_code_base64": qr_base64
        }, status=status.HTTP_201_CREATED)


class EmailMFASetupView(APIView):
    permission_classes = [AppSecretKeyPermission]

    def post(self, request):
        developer_app = request.developer_app
        external_user_id = request.data.get("external_user_id")
        email = request.data.get("email")

        if not external_user_id or not email:
            return Response(
                {"error": "external_user_id and email are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        client, _ = Client.objects.get_or_create(
            developer_app=developer_app,
            external_user_id=external_user_id,
            defaults={
                "mfa_type": "email",
                "email": email,
                "is_active": True
            }
        )

        # In case MFA type was changed later
        client.mfa_type = "email"
        client.email = email
        client.is_active = True
        client.save()

        return Response({
            "success": True,
            "message": "Email MFA setup completed"
        }, status=status.HTTP_201_CREATED)


class EmailOTPSendView(APIView):
    permission_classes = [AppSecretKeyPermission]

    def post(self, request):
        developer_app = request.developer_app
        external_user_id = request.data.get("external_user_id")

        if not external_user_id:
            return Response({"error": "external_user_id required"}, status=400)

        try:
            client = Client.objects.get(
                developer_app=developer_app,
                external_user_id=external_user_id,
                mfa_type="email",
                is_active=True
            )
        except Client.DoesNotExist:
            return Response({"error": "Email MFA not setup"}, status=404)

        if not client.email:
            return Response({"error": "No email registered"}, status=400)

        otp = f"{random.randint(100000, 999999)}"
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()

        EmailOTP.objects.create(
            client=client,
            email=client.email,
            otp_hash=otp_hash,
            expires_at=timezone.now() + timedelta(minutes=5),
        )

        send_mail(
            subject="Your verification code",
            message=f"Your verification code is {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[client.email],
        )

        return Response({
            "success": True,
            "message": "OTP sent"
        })


class EmailOTPVerifyView(APIView):
    permission_classes = [AppSecretKeyPermission]

    def post(self, request):
        developer_app = request.developer_app
        external_user_id = request.data.get("external_user_id")
        otp = request.data.get("otp")

        if not external_user_id or not otp:
            return Response({"error": "Missing data"}, status=400)

        try:
            client = Client.objects.get(
                developer_app=developer_app,
                external_user_id=external_user_id,
                mfa_type="email"
            )
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=404)

        otp_hash = hashlib.sha256(otp.encode()).hexdigest()

        email_otp = EmailOTP.objects.filter(
            client=client,
            otp_hash=otp_hash,
            is_used=False
        ).order_by("-created_at").first()

        if not email_otp or email_otp.is_expired():
            return Response({"error": "Invalid or expired OTP"}, status=400)

        email_otp.is_used = True
        email_otp.save()

        return Response({
            "success": True,
            "verified": True
        })
