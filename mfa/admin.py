from django.contrib import admin
from .models import *
admin.site.register(TOTPDevice)
admin.site.register(EmailOTP)
admin.site.register(Client)