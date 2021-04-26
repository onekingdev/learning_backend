from .models import Topic
from django.contrib import admin
from cnt.questions.models import Question
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline

class QuestionInline(TranslatableTabularInline):
    model = Question

class TopicAdminForm(MPTTAdminForm, TranslatableModelForm):
    pass

@admin.register(Topic)
class TopicAdmin(DraggableMPTTAdmin, TranslatableAdmin):
    search_fields = ['translations__name', 'standard_code']
    form =  TopicAdminForm
    inlines = [
        QuestionInline,
    ]
    list_display = ['tree_actions', 'indented_title', 'standard_code', 'area_of_knowledge', 'question_count']

    def question_count(self, instance):
        return Question.objects.filter(topic__in=instance.get_descendants(include_self=True)).count()