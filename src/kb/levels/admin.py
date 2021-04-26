from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline
from .models import Level
from import_export.admin import ImportExportModelAdmin

@admin.register(Level)
class LevelAdmin(TranslatableAdmin):
    pass
