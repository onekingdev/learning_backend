from django.contrib import admin
from .models import Audience
from parler import admin as parler_admin
from import_export.admin import ImportExportModelAdmin
from .resources import AudienceResource


@admin.register(Audience)
class AudienceAdmin(ImportExportModelAdmin, parler_admin.TranslatableAdmin):
    resource_class = AudienceResource

    list_display = ('id', 'name', 'slug', 'standard_code')
    search_fields = ('name', 'slug',)
    list_filter = ('standard_code', 'slug')
    fieldsets = ()
