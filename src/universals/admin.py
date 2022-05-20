from django.contrib import admin
from .models.topics import UniversalTopic
from .models.areas_of_knowledge import UniversalAreaOfKnowledge


@admin.register(UniversalTopic)
class UniversalTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'area_of_knowledge', 'parent', 'standard_code')
    search_fields = ('name', 'area_of_knowledge', 'standard_code')
    list_filter = ('area_of_knowledge', 'slug')


@admin.register(UniversalAreaOfKnowledge)
class UniversalAreaOfKnowledgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug')
    search_fields = ('id', 'slug',)
    list_filter = ('slug',)
