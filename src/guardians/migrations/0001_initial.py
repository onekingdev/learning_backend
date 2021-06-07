# Generated by Django 3.2.3 on 2021-06-01 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
                ('last_name', models.CharField(max_length=128, null=True)),
                ('gender', models.CharField(max_length=128, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='GuardianStudent',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('guardian', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='guardians.guardian')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='students.student')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]