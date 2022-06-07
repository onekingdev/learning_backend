from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html

from pathlib import Path
import io

from .models import DatabaseBackup

@admin.register(DatabaseBackup)
class DatabaseBackupAdmin(admin.ModelAdmin):
    list_display = ('id', 'backup_name', 'backup_filename', 'download_link', 'backup_date')
    search_fields = ('id', 'backup_name', 'backup_filename')
    list_filter = ('backup_date',)
    readonly_fields = ('download_link', 'backup_date')

    def get_urls(self):
        urls = super(DatabaseBackupAdmin, self).get_urls()
        urls += [
            url(r'^download/(?P<pk>\d+)$', self.download_file,
                name='backups_databasebackup_download'),
        ]
        return urls

    def download_link(self, obj):
        if obj.id is not None:
            return format_html(
                '<a href="{}">Download</a>',
                reverse('admin:backups_databasebackup_download', args=[obj.pk])
            )
        return "-"
    download_link.short_description = "Backup download"

    def download_file(self, request, pk):
        database_backup = DatabaseBackup.objects.get(pk=pk)
        output_filename = database_backup.backup_filename
        backup_filepath = f'{Path(__file__).resolve().parent.parent}/backups/database_backup/{output_filename}'

        output_filesource = ''
        with io.open(backup_filepath, 'r', encoding='utf-8') as f:
            output_filesource = f.read()

        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename={output_filename}'
        response.write(output_filesource.encode("utf-8"))
        return response
