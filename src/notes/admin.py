from django.contrib import admin

from notes.models import Notes
from import_export import admin as import_export_admin

@admin.register(Notes)
class NotesAdmin(
        import_export_admin.ImportExportModelAdmin,
):
    list_display = (
            'title',
            'user_from',
            'user_to',
            'send_at'
    )
# Register your models here.
