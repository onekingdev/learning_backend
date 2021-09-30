from import_export.resources import ModelResource
from import_export.fields import Field
from .models import Question
from app.resources import LangField


class ChildModelByNumber(LangField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QuestionAdminResource(ModelResource):
    language_code = Field(
        attribute='get_current_language'
    )
    name = LangField(
        attribute='question_text'
    )

    answer_option_1 = ChildModelByNumber(
        attribute='answeroption__answer_text',
        position=1
    )

    class Meta:
        model = Question
        skip_unchanged = True
        report_skipped = False
