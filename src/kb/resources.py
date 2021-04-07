from import_export import resources
from import_export.fields import Field
from .models import Question

class QuestionAdminResource(resources.ModelResource):
    question_text = Field(attribute='question_text')
    answer_1 = Field()
    class Meta:
        model = Question
        fields = ['id', 'topic']

    def dehydrate_answer_1(self, obj):
        try:
            return obj.answeroption_set.all().first().answer_text
        except:
            return ''




    def after_import_row(row, row_result, row_number=None, **kwargs):
        pass
