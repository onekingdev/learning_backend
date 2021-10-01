from import_export.resources import ModelResource
from import_export.fields import Field
from .models import Question
from app.resources import LangField


class QuestionResource(ModelResource):
    language_code = Field(
        attribute='get_current_language'
    )

    name = LangField(
        attribute='question_text'
    )

    class Meta:
        model = Question
        skip_unchanged = True
        report_skipped = False
