from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline
from .models import AnswerOption
from import_export.admin import ImportExportModelAdmin

class AnswerOptionInline(TranslatableStackedInline):
    model = AnswerOption
