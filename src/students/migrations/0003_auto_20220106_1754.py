# Generated by Django 3.2.11 on 2022-01-07 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_initial'),
        ('plans', '0001_initial'),
        ('students', '0002_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='active_student_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='active_student_plan', to='plans.studentplan'),
        ),
        migrations.AlterField(
            model_name='student',
            name='active_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='active_group', to='organization.group'),
        ),
    ]
