# Generated by Django 3.2.12 on 2022-03-04 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoinWallet',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.account')),
            ],
            options={
                'abstract': False,
            },
            bases=('accounting.account',),
        ),
    ]
