# Generated by Django 3.2.11 on 2022-01-05 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('block', '0001_initial'),
        ('kb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockquestionpresentation',
            name='chosen_answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='kb.answeroption'),
        ),
        migrations.AddField(
            model_name='blockquestionpresentation',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kb.question'),
        ),
        migrations.AddField(
            model_name='blockquestionpresentation',
            name='topic_grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kb.topicgrade'),
        ),
        migrations.AddField(
            model_name='blockpresentation',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='block.block'),
        ),
    ]
