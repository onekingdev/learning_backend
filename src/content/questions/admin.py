from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline
from .models import Question, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset
from import_export.admin import ImportExportModelAdmin
from .resources import QuestionAdminResource

# Register your models here.


class QuestionInline(TranslatableTabularInline):
    model = Question

class QuestionImageAssetInline(admin.StackedInline):
    model = QuestionImageAsset
class QuestionVideoAssetInline(admin.StackedInline):
    model = QuestionVideoAsset
class QuestionAudioAssetInline(admin.StackedInline):
    model = QuestionAudioAsset

@admin.register(Question)
class QuestionAdmin(TranslatableAdmin, ImportExportModelAdmin):
    resource_class = QuestionAdminResource
    autocomplete_fields = ['topic']
    inlines = [
        QuestionImageAssetInline,
        QuestionVideoAssetInline,
        QuestionAudioAssetInline,
        AnswerOptionInline,
    ]