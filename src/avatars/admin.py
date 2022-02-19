from django.contrib import admin
from .models import Avatar
from .resources import AvatarResource
from import_export import admin as import_export_admin

@admin.register(Avatar)
class AvatarAdmin(
        import_export_admin.ImportExportModelAdmin,
):
    resource_class = AvatarResource
    list_display = [
        'name',
        'type_of',
        'price',
    ]
