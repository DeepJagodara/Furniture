# api/admin.py

from django.contrib import admin
from .models import Furniture,UserProfile

admin.site.register(Furniture)
admin.site.register(UserProfile)