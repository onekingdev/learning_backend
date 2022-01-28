from django.contrib import admin
from .models import Topic, AreaOfKnowledge, Grade, TopicGrade
from .models.content import Question, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset, QuestionTTSAsset
from .models.content import AnswerOption

from . import resources
from parler import admin as parler_admin
from import_export import admin as import_export_admin
from mptt.admin import DraggableMPTTAdmin


class AnswerOptionInline(parler_admin.TranslatableStackedInline):
    model = AnswerOption
    extra = 0


class QuestionImageAssetInline(admin.TabularInline):
    model = QuestionImageAsset
    extra = 0


class QuestionVideoAssetInline(admin.TabularInline):
    model = QuestionVideoAsset
    extra = 0


class QuestionAudioAssetInline(admin.TabularInline):
    model = QuestionAudioAsset
    extra = 0


class QuestionTTSAssetInline(admin.TabularInline):
    model = QuestionTTSAsset
    extra = 0


@admin.action(description='Hard delete objects')
def hard_delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.hard_delete()


@admin.register(Topic)
class TopicAdmin(
        parler_admin.TranslatableAdmin,
        import_export_admin.ImportExportModelAdmin,
        DraggableMPTTAdmin,
):
    resource_class = resources.TopicResource
    list_display = (
        'tree_actions',
        'indented_title',
        'area_of_knowledge',
        'create_timestamp',
        'update_timestamp'
    )
    actions = [hard_delete_selected]


@admin.register(AreaOfKnowledge)
class AreaOfKnowledgeAdmin(import_export_admin.ImportExportModelAdmin, parler_admin.TranslatableAdmin):
    resource_class = resources.AreaOfKnowledgeResource
    list_display = (
        'name',
        'audience',
        'universal_area_knowledge',
    )


@admin.register(Grade)
class GradeAdmin(
        parler_admin.TranslatableAdmin,
        import_export_admin.ImportExportModelAdmin):
    resource_class = resources.GradeResource
    list_display = (
        'name',
        'id',
        'audience',
    )


@admin.register(TopicGrade)
class TopicGradeAdmin(
        import_export_admin.ImportExportModelAdmin):
    resource_class = resources.TopicGradeResource
    list_display = (
        'topic',
        'grade',
        'grade_audience'
    )
    list_filter = (
        'grade__audience',
    )


@admin.register(AnswerOption)
class AnswerOptionAdmin(
        parler_admin.TranslatableAdmin,
        import_export_admin.ImportExportModelAdmin):
    resource_class = resources.AnswerOptionResource


@admin.register(Question)
class QuestionAdmin(parler_admin.TranslatableAdmin, import_export_admin.ImportExportModelAdmin):
    resource_class = resources.QuestionResource
    inlines = [AnswerOptionInline,
               QuestionImageAssetInline,
               QuestionVideoAssetInline,
               QuestionTTSAssetInline,
               QuestionAudioAssetInline]
    fields = (
        'question_text',
        'topic',
        'grade',
    )
    list_display = (
        'question',
        'topic',
        'grade',
        'grade_audience',
    )
    list_filter = (
        'grade__audience',
    )


@admin.register(QuestionImageAsset)
class QuestionImageAssetAdmin(import_export_admin.ImportExportModelAdmin):
    resource_class = resources.QuestionImageAssetResource
