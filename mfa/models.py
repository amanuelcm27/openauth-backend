from django.utils import timezone
import uuid
import pyotp
from django.db import models
from developers.models import DeveloperApp


class Client(models.Model):
    MFA_TYPES = (
        ("totp", "TOTP"),
        ("email", "Email OTP"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    developer_app = models.ForeignKey(
        DeveloperApp, on_delete=models.CASCADE, related_name="clients")

    # This links to developer's own user ID
    external_user_id = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    
    mfa_type = models.CharField(max_length=10, choices=MFA_TYPES)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.external_user_id} ({self.mfa_type})"


class TOTPDevice(models.Model):
    client = models.OneToOneField(
        Client, on_delete=models.CASCADE, related_name="totp_device")
    secret_key = models.CharField(max_length=32)  # Base32 secret

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_secret():
        return pyotp.random_base32()

    def __str__(self):
        return f"TOTP for {self.client.external_user_id}"


class EmailOTP(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="email_otps")

    email = models.EmailField()
    otp_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.expires_at
