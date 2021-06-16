# Generated by Django 3.2.3 on 2021-06-16 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20210604_1158'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='avatar',
            options={},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={},
        ),
        migrations.RemoveField(
            model_name='avatar',
            name='path',
        ),
        migrations.AddField(
            model_name='avatar',
            name='image',
            field=models.ImageField(blank=True, help_text='The image of the avatar', null=True, upload_to=''),
        ),
    ]
