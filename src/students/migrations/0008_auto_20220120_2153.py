# Generated by Django 3.2.11 on 2022-01-21 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_alter_avatar_type_of'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar_accessories',
            field=models.ForeignKey(limit_choices_to={'type_of': 'ACCESSORIES'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='students.avatar'),
        ),
        migrations.AlterField(
            model_name='student',
            name='avatar_clothes',
            field=models.ForeignKey(limit_choices_to={'type_of': 'CLOTHES'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='students.avatar'),
        ),
        migrations.AlterField(
            model_name='student',
            name='avatar_head',
            field=models.ForeignKey(limit_choices_to={'type_of': 'HEAD'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='students.avatar'),
        ),
        migrations.AlterField(
            model_name='student',
            name='avatar_pants',
            field=models.ForeignKey(limit_choices_to={'type_of': 'PANTS'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='students.avatar'),
        ),
    ]
