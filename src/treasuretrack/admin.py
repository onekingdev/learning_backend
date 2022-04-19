from django.contrib import admin
from .models import DailyTreasureLevel
from adminsortable2.admin import SortableAdminMixin


@admin.register(DailyTreasureLevel)
class DailyTreasureLevelAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = ['level']
    list_display = ['name', 'coins_required', 'level']
