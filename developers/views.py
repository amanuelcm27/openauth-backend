from .serializers import DeveloperAppCreateSerializer
from .models import Developer, DeveloperApp
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Developer
from .serializers import DeveloperRegisterSerializer, DeveloperAppCreateSerializer


class DeveloperRegisterView(APIView):
    def post(self, request):
        serializer = DeveloperRegisterSerializer(data=request.data)
        if serializer.is_valid():
            developer = serializer.save()
            return Response({
                "success": True,
                "developer_api_key": developer.developer_api_key,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeveloperAPIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        key = request.headers.get("X-Developer-Key")
        if not key:
            return False
        try:
            developer = Developer.objects.get(developer_api_key=key)
            request.developer = developer
            return True
        except Developer.DoesNotExist:
            return False


class DeveloperAppCreationView(APIView):
    permission_classes = [DeveloperAPIKeyPermission]

    def post(self, request):
        serializer = DeveloperAppCreateSerializer(data=request.data)
        if serializer.is_valid():
            developer = request.developer
            app = serializer.save(developer=developer)
            return Response({
                "success": True,
                "app_id": str(app.id),
                "app_secret_key": app.app_secret_key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
