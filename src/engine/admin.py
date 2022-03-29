from django.contrib import admin
from .models import TopicMasterySettings

# Register your models here.
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
