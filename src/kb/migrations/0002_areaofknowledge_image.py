# Generated by Django 3.2.3 on 2021-06-04 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='areaofknowledge',
            name='image',
            field=models.TextField(null=True),
        ),
    ]