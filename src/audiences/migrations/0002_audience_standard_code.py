# Generated by Django 3.2.11 on 2022-01-14 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audience',
            name='standard_code',
            field=models.CharField(max_length=4, null=True),
        ),
    ]