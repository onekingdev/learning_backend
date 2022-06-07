import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent + '/backups/'

DBBACKUP_STORAGE_OPTIONS = { 'location': BASE_DIR / 'backups' / 'database_backup' }

print(DBBACKUP_STORAGE_OPTIONS)