from app.resources import TranslatableModelResource
from import_export.fields import Field
from .models import Topic
from .models.content import Question


class TopicResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
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
