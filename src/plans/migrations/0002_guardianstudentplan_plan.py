# Generated by Django 3.2.11 on 2022-02-16 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guardians', '0004_alter_guardian_user'),
        ('kb', '0013_areaofknowledge_is_active'),
        ('students', '0014_auto_20220214_1455'),
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('area_of_knowledge', models.CharField(choices=[('ALL', 'ALL'), ('ONE', 'ONE'), ('TWO', 'TWO')], default='ALL', max_length=255)),
                ('slug', models.SlugField(editable=False)),
                ('price_month', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('price_year', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('currency', models.CharField(max_length=4)),
                ('is_cancel', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GuardianStudentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('slug', models.SlugField(editable=False)),
                ('cancel_reason', models.TextField(blank=True)),
                ('is_cancel', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('expired_at', models.DateTimeField(null=True)),
                ('period', models.CharField(choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')], max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('guardian', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='guardians.guardian')),
                ('plan', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='plans.plan')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='students.student')),
                ('subject', models.ManyToManyField(blank=True, to='kb.AreaOfKnowledge')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]