# Generated by Django 3.2.3 on 2021-06-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audience',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
    ]
