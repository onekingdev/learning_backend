# Generated by Django 3.2.4 on 2021-07-06 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionasset',
            name='order',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
