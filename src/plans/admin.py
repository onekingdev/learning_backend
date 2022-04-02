from django.contrib import admin
from import_export import admin as import_export_admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(
        import_export_admin.ImportExportModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'area_of_knowledge',
        'price_month',
        'price_year',
        'currency',
    )
