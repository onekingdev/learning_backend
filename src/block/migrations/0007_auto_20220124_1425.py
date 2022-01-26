# Generated by Django 3.2.11 on 2022-01-24 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('block', '0006_auto_20220118_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockpresentation',
            name='errors',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blockpresentation',
            name='hits',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blockpresentation',
            name='start_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='blockpresentation',
            name='total',
            field=models.IntegerField(default=0, null=True),
        ),
    ]