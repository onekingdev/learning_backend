from django.contrib import admin
from .models import TopicMasterySettings
from admin_auto_filters.filters import AutocompleteFilter


class TopicFilter(AutocompleteFilter):
    title = 'Topic'
    field_name = 'topic'

@admin.register(TopicMasterySettings)
class TopicMasterySettingsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'topic',
        'sample_size',
        'mastery_percentage',
        'competence_percentage',
    )
    list_filter = (
        'topic__area_of_knowledge__universal_area_knowledge',
    )
    # list_filter = [TopicFilter]
