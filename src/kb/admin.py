from django.contrib import admin
from .models import Topic, AreaOfKnowledge, Grade
from .models.content import Question, AnswerOption, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset

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
class AreaOfKnowledgeAdmin(parler_admin.TranslatableAdmin):
    list_display = (
        'name',
        'audience',
        'universal_area_knowledge',
    )


@admin.register(Grade)
class GradeAdmin(parler_admin.TranslatableAdmin):
    pass


@admin.register(AnswerOption)
class AnswerOptionAdmin(parler_admin.TranslatableAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(parler_admin.TranslatableAdmin,
                    import_export_admin.ImportExportModelAdmin):
    resource_class = resources.QuestionResource
    inlines = [AnswerOptionInline,
               QuestionImageAssetInline,
               QuestionVideoAssetInline,
               QuestionAudioAssetInline]
