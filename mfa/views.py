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
            return Response({"error": "external_user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

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

        # Generate QR code as image in memory
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
            "qr_code_base64": qr_base64  # frontend can directly display this
        }, status=status.HTTP_201_CREATED)
