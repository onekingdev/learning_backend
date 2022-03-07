# Generated by Django 3.2.12 on 2022-03-04 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_alter_studenttopicmastery_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenttopicmastery',
            name='mastery_level',
            field=models.CharField(choices=[('NP', 'Not practiced'), ('N', 'Novice'), ('C', 'Competent'), ('M', 'Master')], default='NP', max_length=3),
        ),
    ]
