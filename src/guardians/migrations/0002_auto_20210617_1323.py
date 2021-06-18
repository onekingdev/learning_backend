# Generated by Django 3.2.3 on 2021-06-17 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guardians', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guardian',
            options={},
        ),
        migrations.AlterField(
            model_name='guardian',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], max_length=8, null=True),
        ),
    ]
