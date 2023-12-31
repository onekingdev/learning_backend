# Generated by Django 3.2.12 on 2022-05-25 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0007_auto_20220525_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.order'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
