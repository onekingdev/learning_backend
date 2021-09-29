from import_export.resources import ModelResource
from import_export.fields import Field
from .models import Topic
from parler.utils.context import switch_language


class LangField(Field):
    def clean(self, obj, data, is_m2m=False):
        print('ahua', self, obj, data)
        #with switch_language(obj, lang):
        super().clean(obj, data, is_m2m=is_m2m)
        

class TopicAdminResource(ModelResource):
    language_code = Field(
    )
    name = LangField(
    )

    class Meta:
        model = Topic
        # fields = ['area_of_knowledge', 'parent', 'name', 'translations__name']
        skip_unchanged = True
        report_skipped = False
        exclude = ['parent']

    def before_import_row(self, *args, **kwargs):
        lang = args[0]['language_code']
        self.LANG = lang
        super().before_import_row(*args, **kwargs)

    def before_save_instance(self, *args, **kwargs):
        super().before_save_instance(*args, **kwargs)





