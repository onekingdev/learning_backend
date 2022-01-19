from django.contrib import admin
from .models import Audience
from parler import admin as parler_admin


@admin.register(Audience)
class AudienceAdmin(parler_admin.TranslatableAdmin):
    pass
