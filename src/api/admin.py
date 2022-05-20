from django.contrib import admin
from .models import profile


class AdminProfileInline(admin.StackedInline):
    model = profile
    can_delete = False
