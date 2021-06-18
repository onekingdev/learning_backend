# Generated by Django 3.2.3 on 2021-06-17 09:13

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kb', '0001_initial'),
        ('content', '0001_initial'),
        ('students', '0001_initial'),
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
                ('modality', models.CharField(choices=[('AI', 'AI'), ('PATH', 'Choose your path'), ('PRACTICE', 'Practice')], default='AI', max_length=128)),
                ('first_presentation_timestamp', models.DateTimeField(null=True)),
                ('last_presentation_timestamp', models.DateTimeField(null=True)),
                ('engangement_points_available', models.PositiveSmallIntegerField(null=True)),
                ('coins_available', models.PositiveSmallIntegerField(null=True)),
                ('battery_points_available', models.PositiveSmallIntegerField(null=True)),
                ('engangement_points_earned', models.PositiveSmallIntegerField(null=True)),
                ('coins_earned', models.PositiveSmallIntegerField(null=True)),
                ('battery_points_earned', models.PositiveSmallIntegerField(null=True)),
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
                ('name', models.CharField(max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('is_correct', models.BooleanField(null=True)),
                ('is_answered', models.BooleanField(default=False, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CORRECT', 'Correct'), ('INCORRECT', 'Incorrect')], default='PENDING', max_length=128)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.block')),
                ('chosen_answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.answeroption')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='content.question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlockTypeConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('data_type', models.CharField(max_length=128, null=True)),
                ('value', models.CharField(max_length=128, null=True)),
                ('block_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blocktype')),
                ('key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blockconfigurationkeyword')),
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
            name='BlockPresentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('hits', models.IntegerField(null=True)),
                ('errors', models.IntegerField(null=True)),
                ('total', models.IntegerField(null=True)),
                ('points', models.IntegerField(null=True)),
                ('start_timestamp', models.DateTimeField(null=True)),
                ('end_timestamp', models.DateTimeField(null=True)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='block.block')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlockConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('data_type', models.CharField(max_length=128, null=True)),
                ('value', models.CharField(max_length=128, null=True)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.block')),
                ('key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blockconfigurationkeyword')),
            ],
            options={
                'abstract': False,
            },
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
            field=models.ManyToManyField(blank=True, help_text='These are the topics covered in this block', to='kb.Topic'),
        ),
        migrations.AddField(
            model_name='block',
            name='type_of',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='block.blocktype'),
        ),
        migrations.CreateModel(
            name='BlockTypeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=128, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='block.blocktype')),
            ],
            options={
                'verbose_name': 'block type Translation',
                'db_table': 'block_blocktype_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
