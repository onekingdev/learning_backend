# Generated by Django 3.2.3 on 2021-06-01 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='student',
            field=models.ManyToManyField(blank=True, to='students.Student'),
        ),
    ]