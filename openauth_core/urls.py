
from django.contrib import admin 
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('developers/', include('developers.urls')),
    path('mfa/', include('mfa.urls')),
]
