from django.urls import path
from .views import TOTPSetupView

urlpatterns = [
    path("totp/setup/", TOTPSetupView.as_view(), name="totp-setup"),
]
