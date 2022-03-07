# Generated by Django 3.2.12 on 2022-03-04 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankwallet',
            name='student',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bankWallet', to='students.student'),
        ),
    ]
