from django.contrib import admin
from import_export import admin as import_export_admin
from .models import Plan, GuardianStudentPlan


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

@admin.register(GuardianStudentPlan)
class GuardianStudentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        "student",
        'guardian',
        'plan',
        'is_cancel',
        'is_paid',
        'expired_at'
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)