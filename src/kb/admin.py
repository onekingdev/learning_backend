from django.contrib import admin
from .models import  Topic, AreaOfKnowledge
from parler import admin as parler_admin



# Register your models here.
@admin.register(Topic)
class TopicAdmin(parler_admin.TranslatableAdmin):
    pass


@admin.register(AreaOfKnowledge)
class AreaOfKnowledgeAdmin(parler_admin.TranslatableAdmin):
    pass

