# Generated by Django 3.2.11 on 2022-02-07 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0010_alter_student_user'),
        ('wallets', '0003_alter_coinwallet_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.UUIDField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('type_of', models.CharField(choices=[('ACCESSORIES', 'Accessories'), ('HEAD', 'Head/Hair'), ('CLOTHES', 'Clothes'), ('PANTS', 'Pants')], max_length=25, null=True)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('image', models.URLField(null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('in_use', models.BooleanField(default=False)),
                ('avatar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='avatars.avatar')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='students.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AvatarPurchaseTransaction',
            fields=[
                ('withdraw_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wallets.withdraw')),
                ('avatar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='avatars.avatar')),
            ],
            options={
                'abstract': False,
            },
            bases=('wallets.withdraw',),
        ),
    ]
