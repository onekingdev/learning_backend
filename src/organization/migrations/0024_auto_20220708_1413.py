# Generated by Django 3.2.13 on 2022-07-08 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0023_auto_20220708_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherclassroom',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.classroom'),
        ),
        migrations.AlterField(
            model_name='teacherclassroom',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.teacher'),
        ),
    ]
