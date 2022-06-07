from django.conf import settings
from django.db import models
from django.http.response import HttpResponse
from django.utils.html import mark_safe
from pathlib import Path
import mimetypes
import os

class DatabaseBackup(models.Model):
    id = models.AutoField(primary_key=True)
    backup_name = models.CharField(max_length=64)
    backup_filename = models.CharField(max_length=255)
    backup_date = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.backup_name)
