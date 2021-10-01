from import_export.resources import ModelResource
from import_export.fields import Field
from .models import Topic
from app.resources import LangField


class TopicResource(ModelResource):
    language_code = Field(
        attribute='get_current_language'
    )

    name = LangField(
        attribute='name'
    )

    class Meta:
        model = Topic
        # fields = ['area_of_knowledge', 'parent', 'name', 'translations__name']
        skip_unchanged = True
        report_skipped = False
        exclude = ['parent']

    def before_import_row(self, row, row_number=None, **kwargs):
        pass
