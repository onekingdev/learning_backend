# Generated by Django 3.2.11 on 2022-02-14 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0008_alter_block_topic_grade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='engangement_points_available',
            new_name='experience_points_available',
        ),
        migrations.RemoveField(
            model_name='block',
            name='battery_points_available',
        ),
    ]