# Generated by Django 3.2.3 on 2021-06-01 17:12

from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
        ('kb', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('modality', models.CharField(choices=[('AI', 'AI'), ('PATH', 'Choose your path'), ('PRACTICE', 'Practice')], default='AI', max_length=128)),
                ('first_presentation_timestamp', models.DateTimeField(null=True)),
                ('last_presentation_timestamp', models.DateTimeField(null=True)),
                ('engangement_points', models.IntegerField(null=True)),
                ('coins_earned', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlockConfigurationKeyword',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
                ('slug', models.SlugField(editable=False)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlockPresentation',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hits', models.IntegerField(null=True)),
                ('errors', models.IntegerField(null=True)),
                ('total', models.IntegerField(null=True)),
                ('points', models.IntegerField(null=True)),
                ('start_timestamp', models.DateTimeField(null=True)),
                ('end_timestamp', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['create_timestamp'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlockQuestion',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_correct', models.BooleanField(null=True)),
                ('is_answered', models.BooleanField(default=False, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Correct', 'Correct'), ('Incorrect', 'Incorrect')], default='Pending', max_length=128)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.block')),
                ('chosen_answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='content.answeroption')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='content.question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockType',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
                ('slug', models.SlugField(editable=False)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlockTypeConfiguration',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_type', models.CharField(max_length=128, null=True)),
                ('value', models.CharField(max_length=128, null=True)),
                ('block_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blocktype')),
                ('key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blockconfigurationkeyword')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlockQuestionPresentation',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('presentation_timestamp', models.DateTimeField(null=True)),
                ('submission_timestamp', models.DateTimeField(null=True)),
                ('block_question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blockquestion')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='content.question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockConfiguration',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_type', models.CharField(max_length=128, null=True)),
                ('value', models.CharField(max_length=128, null=True)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.block')),
                ('key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blockconfigurationkeyword')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='block',
            name='questions',
            field=models.ManyToManyField(through='block.BlockQuestion', to='content.Question'),
        ),
        migrations.AddField(
            model_name='block',
            name='student',
            field=models.ManyToManyField(blank=True, to='students.Student'),
        ),
        migrations.AddField(
            model_name='block',
            name='topics',
            field=models.ManyToManyField(blank=True, to='kb.Topic'),
        ),
        migrations.AddField(
            model_name='block',
            name='type_of',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blocktype'),
        ),
    ]
