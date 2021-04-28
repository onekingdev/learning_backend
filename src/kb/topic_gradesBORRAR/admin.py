from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline
from .models import TopicGrade
from import_export.admin import ImportExportModelAdmin

class TopicGradeAdmin(TranslatableStackedInline):
    model = TopicGrade
