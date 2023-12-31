# Generated by Django 3.2.12 on 2022-05-25 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0005_alter_guardianstudentplan_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardianstudentplan',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created timestamp'),
        ),
        migrations.AlterField(
            model_name='guardianstudentplan',
            name='update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated timestamp'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created timestamp'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated timestamp'),
        ),
        migrations.AlterField(
            model_name='studentplan',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created timestamp'),
        ),
        migrations.AlterField(
            model_name='studentplan',
            name='update_timestamp',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated timestamp'),
        ),
    ]
