# Generated by Django 3.2.3 on 2021-06-08 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kb', '0002_areaofknowledge_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaofknowledge',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
