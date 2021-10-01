from django.contrib import admin
from .models import Topic, AreaOfKnowledge, Grade
from . import resources
from parler import admin as parler_admin
from import_export import admin as import_export_admin


@admin.register(Topic)
class TopicAdmin(
        parler_admin.TranslatableAdmin,
        import_export_admin.ImportExportModelAdmin,
):
    resource_class = resources.TopicResource
    list_display = ('name', 'create_timestamp', 'update_timestamp')


@admin.register(AreaOfKnowledge)
class AreaOfKnowledgeAdmin(parler_admin.TranslatableAdmin):
    pass


@admin.register(Grade)
class GradeAdmin(parler_admin.TranslatableAdmin):
    pass
