from django.contrib import admin
from .models import Audience
from parler import admin as parler_admin
from import_export.admin import ImportExportModelAdmin
from .resources import AudienceResource


@admin.register(Audience)
class AudienceAdmin(ImportExportModelAdmin, parler_admin.TranslatableAdmin):
    resource = AudienceResource
