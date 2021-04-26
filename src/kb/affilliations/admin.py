from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline
from .models import Affilliation
from import_export.admin import ImportExportModelAdmin

class AffilliationAdmin(TranslatableStackedInline):
    model = Affilliation
