from django.urls import path
from .views import TOTPSetupView, TOTPVerifyView,  EmailMFASetupView, EmailOTPSendView, EmailOTPVerifyView , MFAStatusView

urlpatterns = [
    path("totp/setup/",   TOTPSetupView.as_view(), name="totp-setup"),
    path("totp/verify/",  TOTPVerifyView.as_view(), name="totp-verify"),
    path("email/setup/",  EmailMFASetupView.as_view(), name="email-setup"),
    path("email/send/",   EmailOTPSendView.as_view(), name="email-otp-send"),
    path("email/verify/", EmailOTPVerifyView.as_view(), name="email-otp-verify"),
    path("status/",       MFAStatusView.as_view(), name="mfa-status"),
]
