# Generated by Django 3.2.12 on 2022-03-04 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kb', '0003_alter_prerequisite_prerequisites'),
        ('students', '0003_auto_20220304_0908'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentTopicGradeStatus',
            new_name='StudentTopicStatus',
        ),
    ]
