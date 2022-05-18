from django.contrib import admin
from .models import WeeklyTreasureLevel, WeeklyTreasure, StudentWeeklyTreasure, WeeklyTreasureTransaction


@admin.register(WeeklyTreasureLevel)
class WeeklyTreasureLevelAdmin(admin.ModelAdmin):
    ordering = ['level']
    list_display = ('id', 'level', 'name', 'correct_questions_required', 'bonus_coins')
    search_fields = ('name', 'bonus_coins')
    list_filter = ('level', 'bonus_coins', 'correct_questions_required')


@admin.register(WeeklyTreasure)
class WeeklyTreasureAdmin(admin.ModelAdmin):
    ordering = ['level']
    list_display = ('id', 'level')
    search_fields = ('level__name', 'level__level')
    list_filter = ('level', 'coins_awarded', 'collectibles_awarded')


@admin.register(StudentWeeklyTreasure)
class StudentWeeklyTreasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'weekly_treasure')
    search_fields = ('student__user__full_name', 'weekly_treasure__level')
    list_filter = ('weekly_treasure',)


@admin.register(WeeklyTreasureTransaction)
class WeeklyTreasureTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_weekly_treasure')
    search_fields = ('student_weekly_treasure__student__user__full_name',
                     'student_weekly_treasure__weekly_treasure__level')
