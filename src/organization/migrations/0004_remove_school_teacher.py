# Generated by Django 3.2.3 on 2021-06-18 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_alter_organizationpersonnel_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='teacher',
        ),
    ]