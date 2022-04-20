from django.contrib import admin
from .models import DailyTreasureLevel


@admin.register(DailyTreasureLevel)
class DailyTreasureLevelAdmin(admin.ModelAdmin):
    ordering = ['level']
    list_display = ['level', 'name', 'coins_required']
