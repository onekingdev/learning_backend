from django.contrib import admin
from .models import Guardian
from import_export.admin import ImportExportModelAdmin

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    pass
