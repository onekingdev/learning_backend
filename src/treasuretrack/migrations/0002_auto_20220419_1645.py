# Generated by Django 3.2.12 on 2022-04-19 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasuretrack', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailytreasurelevel',
            options={'ordering': ['level']},
        ),
        migrations.AddField(
            model_name='dailytreasurelevel',
            name='name',
            field=models.CharField(default='Test', max_length=128),
            preserve_default=False,
        ),
    ]