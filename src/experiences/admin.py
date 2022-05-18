from django.contrib import admin
from .models import Battery, Level
from parler import admin as parler_admin
from import_export.admin import ImportExportModelAdmin


@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'level')
    search_fields = ('student',)
    list_filter = ('level',)


@admin.register(Level)
class LevelAdmin(parler_admin.TranslatableAdmin):
    list_display = ('id', 'name', 'points_required', 'amount', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active', 'amount',)


