from django.contrib import admin
from .models import DailyTreasureLevel


@admin.register(DailyTreasureLevel)
class DailyTreasureLevelAdmin(admin.ModelAdmin):
    ordering = ['level']
    list_display = ['name', 'coins_required', 'level']
