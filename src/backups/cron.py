from django.core.management import call_command
from backups.models import Backup
from django.utils import timezone

def backup_database():
    current_datetime = timezone.now().strftime('%Y%m%d_%H%M%S')

    backup_name = f'db-backup_${current_datetime}'
    backup_filename = f'{backup_name}.psql'
    
    call_command('dbbackup', '--output-filename', backup_name)

    backup = Backup.objects.create(backup_name=backup_name, backup_file=backup_filename)
    backup.save()
    