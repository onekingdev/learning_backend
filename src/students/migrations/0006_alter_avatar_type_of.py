# Generated by Django 3.2.11 on 2022-01-21 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20220120_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='type_of',
            field=models.IntegerField(choices=[(1, 'Accessories'), (2, 'Head/Hair'), (3, 'Clothes'), (4, 'Pants')], null=True),
        ),
    ]