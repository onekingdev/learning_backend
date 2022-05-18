from django.contrib import admin
from import_export import admin as import_export_admin
from .models import Plan, GuardianStudentPlan, StudentPlan


@admin.register(Plan)
class PlanAdmin(import_export_admin.ImportExportModelAdmin):
    list_display = ('id', 'name', 'description', 'area_of_knowledge', 'price_month', 'price_year', 'currency')
    search_fields = ('name', 'description',)
    list_filter = ('area_of_knowledge', 'currency', 'price_month', 'price_year',)


@admin.register(GuardianStudentPlan)
class GuardianStudentPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'guardian', 'plan', 'is_cancel', 'is_paid', 'expired_at')
    search_fields = ('student', 'guardian',)
    list_filter = ('plan', 'is_paid', 'is_cancel', 'expired_at',)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)


@admin.register(StudentPlan)
class StudentPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'audience')
    search_fields = ('name', 'audience',)
    list_filter = ('topic_grade',)
