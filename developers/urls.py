from django.urls import path
from .views import * 

urlpatterns = [
    path("register/", DeveloperRegisterView.as_view(), name="developer-register"),
    path("create_app/", DeveloperAppCreationView.as_view(), name="developer-app-create"),
]


