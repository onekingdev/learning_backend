# Generated by Django 3.2.12 on 2022-02-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('modality', models.CharField(choices=[('AI', 'AI'), ('PATH', 'Choose your path'), ('HOMEWORK', 'Homework')], default='AI', max_length=128)),
                ('block_size', models.IntegerField(default=10)),
                ('experience_points_available', models.PositiveSmallIntegerField(null=True)),
                ('coins_available', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='BlockConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('value', models.CharField(max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockConfigurationKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockPresentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('hits', models.IntegerField(default=0, null=True)),
                ('errors', models.IntegerField(default=0, null=True)),
                ('total', models.IntegerField(default=0, null=True)),
                ('points', models.IntegerField(null=True)),
                ('bonusCoins', models.IntegerField(default=0, null=True)),
                ('coins', models.IntegerField(default=0, null=True)),
                ('start_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_timestamp', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockQuestionPresentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CORRECT', 'Correct'), ('INCORRECT', 'Incorrect')], default='PENDING', max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
