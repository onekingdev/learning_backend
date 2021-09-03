# Generated by Django 3.2.5 on 2021-09-03 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_alter_schoolpersonnel_gender'),
        ('students', '0005_student_avatar_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='active_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ActiveGroup', to='organization.group'),
        ),
    ]
