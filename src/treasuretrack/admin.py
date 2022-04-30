from django.contrib import admin
from .models import WeeklyTreasureLevel


@admin.register(WeeklyTreasureLevel)
class WeeklyTreasureLevelAdmin(admin.ModelAdmin):
    ordering = ['level']
    list_display = ['level', 'name', 'correct_questions_required', 'bonus_coins']
