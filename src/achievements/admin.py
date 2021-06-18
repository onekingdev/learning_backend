from django.contrib import admin
from .models import Achievement
from parler import admin as parler_admin

# Register your models here.
@admin.register(Achievement)
class AchievementAdmin(parler_admin.TranslatableAdmin):
    pass
