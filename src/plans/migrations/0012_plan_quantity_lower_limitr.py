# Generated by Django 3.2.13 on 2022-08-03 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0011_auto_20220803_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='quantity_lower_limitr',
            field=models.IntegerField(default=1),
        ),
    ]
