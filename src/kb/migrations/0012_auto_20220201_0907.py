# Generated by Django 3.2.11 on 2022-02-01 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kb', '0011_auto_20220201_0846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areaofknowledge',
            name='deleted_timestamp',
        ),
        migrations.RemoveField(
            model_name='areaofknowledge',
            name='is_active',
        ),
    ]
