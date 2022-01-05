# Generated by Django 3.2.11 on 2022-01-05 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kb', '0001_initial'),
        ('students', '0001_initial'),
        ('organization', '0001_initial'),
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolpersonnel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='school',
            name='group',
            field=models.ManyToManyField(blank=True, to='organization.Group'),
        ),
        migrations.AddField(
            model_name='school',
            name='organization',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='organization.organization'),
        ),
        migrations.AddField(
            model_name='school',
            name='student',
            field=models.ManyToManyField(blank=True, to='students.Student'),
        ),
        migrations.AddField(
            model_name='school',
            name='student_plan',
            field=models.ManyToManyField(blank=True, to='plans.StudentPlan'),
        ),
        migrations.AddField(
            model_name='organizationpersonnel',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='organization.organization'),
        ),
        migrations.AddField(
            model_name='organizationpersonnel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organization',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_organizations', to='organization.organization'),
        ),
        migrations.AddField(
            model_name='organization',
            name='student_plan',
            field=models.ManyToManyField(to='plans.StudentPlan'),
        ),
        migrations.AddField(
            model_name='group',
            name='area_of_knowledges',
            field=models.ManyToManyField(blank=True, to='kb.AreaOfKnowledge'),
        ),
        migrations.AddField(
            model_name='group',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kb.grade'),
        ),
    ]
