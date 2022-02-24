from django.contrib import admin
from .models import Level
from parler import admin as parler_admin
from import_export.admin import ImportExportModelAdmin


@admin.register(Level)
class LevelAdmin(parler_admin.TranslatableAdmin):
    pass
