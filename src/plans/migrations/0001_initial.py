# Generated by Django 3.2.3 on 2021-06-01 17:01

from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0001_initial'),
        ('kb', '0001_initial'),
        ('audiences', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentPlan',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.SlugField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(editable=False)),
                ('total_credits', models.IntegerField(null=True)),
                ('validity_date', models.DateTimeField(null=True)),
                ('audience', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='audiences.audience')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StudentPlanTopicGrade',
            fields=[
                ('identifier', models.CharField(editable=False, max_length=128, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True, verbose_name='Deleted timestamp')),
                ('random_slug', models.UUIDField(editable=False, unique=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('update_timestamp', models.DateTimeField(auto_now=True, verbose_name='Updated timestamp')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('credit_value', models.IntegerField(null=True)),
                ('is_aproved', models.IntegerField(null=True)),
                ('is_failed', models.IntegerField(null=True)),
                ('question', models.ManyToManyField(to='content.Question')),
                ('student_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='plans.studentplan')),
                ('topic_grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kb.topicgrade')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]