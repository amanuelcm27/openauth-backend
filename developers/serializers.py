from .models import DeveloperApp
from rest_framework import serializers
from .models import Developer
from django.contrib.auth.hashers import make_password


class DeveloperRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Developer
        fields = ["name", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        developer = Developer(**validated_data)
        developer.password_hash = make_password(password)
        developer.save()
        return developer


class DeveloperAppCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperApp
        fields = ["app_name"]
