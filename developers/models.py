import uuid
import secrets
from django.db import models


def generate_api_key():
    return secrets.token_hex(32)  # 64 chars


class Developer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # hashed password since we handle auth manually
    password_hash = models.CharField(max_length=128)

    # used for authenticating developers when they create apps
    developer_api_key = models.CharField(max_length=64, unique=True, default=generate_api_key)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"


class DeveloperApp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name="apps")
    app_name = models.CharField(max_length=150)

    # main key that developers embed inside their mobile apps
    app_secret_key = models.CharField(max_length=64, unique=True, default=generate_api_key)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.app_name} ({self.developer.email})"
