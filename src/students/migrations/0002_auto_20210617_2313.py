# Generated by Django 3.2.3 on 2021-06-18 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avatar',
            name='height',
        ),
        migrations.RemoveField(
            model_name='avatar',
            name='width',
        ),
    ]