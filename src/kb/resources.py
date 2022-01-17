from app.resources import TranslatableModelResource
from app.widgets import TranslatableForeignKeyWidget
from import_export.fields import Field
from import_export.resources import ModelResource
from .models import Topic, Grade, TopicGrade
from .models.content import Question, AnswerOption, QuestionImageAsset
from .models.areas_of_knowledge import AreaOfKnowledge


class AreaOfKnowledgeResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
    )

    class Meta:
        model = AreaOfKnowledge
        skip_unchanged = True
        report_skipped = False


class TopicResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
    )

    parent = Field(
        column_name='parent',
        attribute='parent',
        widget=TranslatableForeignKeyWidget(Topic, 'name')
    )

    class Meta:
        model = Topic
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'language_code',
            'name',
            'is_active',
            'parent',
            'area_of_knowledge',
            'universal_topic',
        )


class GradeResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
    )

    class Meta:
        model = Grade
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'language_code',
            'name',
            'audience',
            'is_active',
        )


class TopicGradeResource(ModelResource):
    topic = Field(attribute='topic__name')
    grade = Field(attribute='grade__name')

    class Meta:
        model = TopicGrade
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'topic',
            'grade',
            'is_active',
        )
        export_order = (
            'id',
            'topic',
            'grade',
            'is_active'
        )


class QuestionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    question_text = Field(attribute='question_text')

    class Meta:
        model = Question
        skip_unchanged = True
        report_skipped = False
        field = (
            'id',
            'identifier',
            'language_code',
            'question_text',
            'topic',
            'grade',
        )
        export_order = (
            'id',
            'identifier',
            'language_code',
            'question_text',
            'topic',
            'grade',
        )
        exclude = (
            'is_active',
            'random_slug',
            'deleted_timestamp',
            'create_timestamp',
            'update_timestamp',
            'topic_grade',
        )


class QuestionImageAssetResource(ModelResource):
    class Meta:
        model = QuestionImageAsset
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'identifier',
            'question__identifier',
            'order',
            'image'
        )
        export_order = (
            'id',
            'identifier',
            'question__identifier',
            'order',
            'image'
        )


class AnswerOptionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    answer_text = Field(
        attribute='answer_text'
    )

    class Meta:
        model = AnswerOption
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'identifier',
            'language_code',
            'answer_text',
            'question__identifier',
            'is_correct',
        )
        export_order = (
            'id',
            'identifier',
            'language_code',
            'answer_text',
            'question__identifier',
            'is_correct',
        )
        exclude = (
            'create_timestamp',
            'update_timestamp',
            'random_slug',
        )
