from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Audience


# Register your models here.
@admin.register(Audience)
class AudienceAdmin(DraggableMPTTAdmin):
    pass
