from app.resources import TranslatableModelResource
from app.widgets import TranslatableForeignKeyWidget
from import_export.fields import Field
from .models import Topic
from .models.content import Question, AnswerOption


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


class QuestionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    class Meta:
        model = Question
        skip_unchanged = True
        report_skipped = False


class AnswerOptionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    class Meta:
        model = AnswerOption
        skip_unchanged = True
        report_skipped = False
