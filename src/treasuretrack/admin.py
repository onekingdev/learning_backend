from django.contrib import admin
from .models import DailyTreasureLevel
from adminsortable2.admin import SortableAdminMixin


@admin.register(DailyTreasureLevel)
class DailyTreasureLevelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['coins_required', 'level']
