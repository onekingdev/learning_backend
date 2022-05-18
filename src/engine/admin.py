from django.contrib import admin
from .models import AreaOfKnowledgeStudentReport, TopicMasterySettings, TopicStudentReport
from admin_auto_filters.filters import AutocompleteFilter


class TopicFilter(AutocompleteFilter):
    title = 'Topic'
    field_name = 'topic'


@admin.register(AreaOfKnowledgeStudentReport)
class AreaOfKnowledgeStudentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'area_of_knowledge', 'student', 'questions_answered', 'correct_question', 'accuracy')
    search_fields = ('student',)
    list_filter = ('area_of_knowledge', 'questions_answered', 'correct_question', 'accuracy',)


@admin.register(TopicMasterySettings)
class TopicMasterySettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'sample_size', 'mastery_percentage', 'competence_percentage',)
    # list_filter = ('topic__area_of_knowledge__universal_area_knowledge',)
    # list_filter = [TopicFilter]


@admin.register(TopicStudentReport)
class TopicStudentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'student', 'questions_answered', 'correct_question', 'accuracy')
    search_fields = ('topic', 'student',)
    list_filter = ('questions_answered', 'correct_question', 'accuracy',)

