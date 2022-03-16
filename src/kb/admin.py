from django.contrib import admin
from .models import Topic, AreaOfKnowledge, Grade, TopicGrade
from .models.content import Question, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset, QuestionTTSAsset
from .models.content import (
    AnswerOption,
    MultipleChoiceAnswerOption,
    OrderAnswerOption,
    RelateAnswerOption,
)
from . import resources

from parler import admin as parler_admin
from import_export import admin as import_export_admin
from polymorphic import admin as polymorphic_admin
from mptt.admin import DraggableMPTTAdmin


class AnswerOptionInline(
    # parler_admin.TranslatableStackedInline,
    polymorphic_admin.StackedPolymorphicInline,
):
    model = AnswerOption

    class MultipleChoiceAnswerOptionInline(
            parler_admin.TranslatableStackedInline,
            polymorphic_admin.StackedPolymorphicInline.Child,
    ):
        model = MultipleChoiceAnswerOption

    class OrderAnswerOptionInline(
        parler_admin.TranslatableStackedInline,
        polymorphic_admin.StackedPolymorphicInline.Child,
    ):
        model = OrderAnswerOption

    class RelateAnswerOptionInline(
        parler_admin.TranslatableStackedInline,
        polymorphic_admin.StackedPolymorphicInline.Child,
    ):
        model = RelateAnswerOption

    child_inlines = (
        MultipleChoiceAnswerOptionInline,
        OrderAnswerOptionInline,
        RelateAnswerOptionInline,
    )


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
        'update_timestamp',
        'id',
    )
    actions = [hard_delete_selected]


@admin.register(AreaOfKnowledge)
class AreaOfKnowledgeAdmin(
        import_export_admin.ImportExportModelAdmin,
        parler_admin.TranslatableAdmin):
    resource_class = resources.AreaOfKnowledgeResource
    list_display = (
        'name',
        'audience',
        'universal_area_knowledge',
        'is_active',
    )
    list_filter = (
        'is_active',
        'audience',
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


@admin.register(MultipleChoiceAnswerOption)
class MultipleChoiceAnswerOptionAdmin(
    parler_admin.TranslatableAdmin,
    import_export_admin.ImportExportModelAdmin,
    polymorphic_admin.PolymorphicChildModelAdmin,
):
    # Import-Export settings
    resource_class = resources.MultipleChoiceAnswerOptionResource

    # Polymorphic settings
    base_model = MultipleChoiceAnswerOption
    show_in_index = True


@admin.register(OrderAnswerOption)
class OrderAnswerOptionAdmin(
    parler_admin.TranslatableAdmin,
    import_export_admin.ImportExportModelAdmin,
    polymorphic_admin.PolymorphicChildModelAdmin,
):
    base_model = OrderAnswerOption
    show_in_index = True


@admin.register(RelateAnswerOption)
class RelateAnswerOptionAdmin(
    parler_admin.TranslatableAdmin,
    import_export_admin.ImportExportModelAdmin,
    polymorphic_admin.PolymorphicChildModelAdmin,
):
    base_model = RelateAnswerOption
    show_in_index = True


@admin.register(AnswerOption)
class AnswerOptionAdmin(
    # parler_admin.TranslatableAdmin,
    import_export_admin.ImportExportModelAdmin,
    polymorphic_admin.PolymorphicParentModelAdmin,
):
    # Display settings
    list_display = (
        # 'answer_text',
        'identifier',
        'question',
        'question_type',
    )
    list_filter = (
        'question__question_type',
    )

    # Import-Export settings
    resource_class = resources.AnswerOptionResource

    # Polymorphic settings
    base_model = AnswerOption
    child_models = (
        MultipleChoiceAnswerOption,
        OrderAnswerOption,
        RelateAnswerOption,
    )


@admin.register(Question)
class QuestionAdmin(
    polymorphic_admin.PolymorphicInlineSupportMixin,
    parler_admin.TranslatableAdmin,
    import_export_admin.ImportExportModelAdmin,
):
    resource_class = resources.QuestionResource
    inlines = [
        AnswerOptionInline,
        QuestionImageAssetInline,
        QuestionVideoAssetInline,
        QuestionTTSAssetInline,
        QuestionAudioAssetInline
    ]
    fields = (
        'question_text',
        'topic',
        'grade',
    )
    list_display = (
        'question',
        'question_type',
        'topic',
        'grade',
        'grade_audience',
    )
    list_filter = (
        'grade__audience',
        'topic__area_of_knowledge',
        'grade',
    )


@admin.register(QuestionImageAsset)
class QuestionImageAssetAdmin(import_export_admin.ImportExportModelAdmin):
    resource_class = resources.QuestionImageAssetResource
    list_display = (
        'question_slug',
        'identifier',
        'image',
    )


@admin.register(QuestionAudioAsset)
class QuestionAudioAssetAdmin(import_export_admin.ImportExportModelAdmin):
    resource_class = resources.QuestionAudioAssetResource
    list_display = (
        'question_slug',
        'identifier',
        'audio_file',
    )
