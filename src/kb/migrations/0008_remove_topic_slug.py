# Generated by Django 3.2.11 on 2022-01-17 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kb', '0007_alter_topictranslation_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='slug',
        ),
    ]
