from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline
from .models import Guardian
from import_export.admin import ImportExportModelAdmin

@admin.register(Guardian)
class GuardianAdmin(TranslatableAdmin):
    pass
