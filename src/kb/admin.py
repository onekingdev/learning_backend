from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline
from .models import Topic, AnswerOption, Question, AreaOfKnowledge, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset, Grade
from import_export.admin import ImportExportModelAdmin
from .resources import QuestionAdminResource

# Register your models here.


class QuestionInline(TranslatableTabularInline):
    model = Question


class TopicAdminForm(MPTTAdminForm, TranslatableModelForm):
    pass

@admin.register(Topic)
class TopicAdmin(DraggableMPTTAdmin, TranslatableAdmin):
    search_fields = ['translations__name', 'standard_code']
    form =  TopicAdminForm
    inlines = [
        QuestionInline,
    ]
    list_display = ['tree_actions', 'indented_title', 'standard_code', 'area_of_knowledge', 'question_count']

    def question_count(self, instance):
        return Question.objects.filter(topic__in=instance.get_descendants(include_self=True)).count()


class AnswerOptionInline(TranslatableStackedInline):
    model = AnswerOption

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

@admin.register(AreaOfKnowledge)
class AreaOfKnowledgeAdmin(TranslatableAdmin):
    pass
@admin.register(Grade)
class GradeAdmin(TranslatableAdmin):
    pass
