from django.contrib import admin
from .models import Audience


# Register your models here.
@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    pass
