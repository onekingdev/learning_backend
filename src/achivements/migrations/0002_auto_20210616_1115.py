# Generated by Django 3.2.3 on 2021-06-16 18:15

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('achivements', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='achivement',
            options={},
        ),
        migrations.RemoveField(
            model_name='achivement',
            name='name',
        ),
        migrations.AlterField(
            model_name='achivement',
            name='hex_color',
            field=models.CharField(blank=True, help_text='The color of the achivement', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='achivement',
            name='image',
            field=models.ImageField(blank=True, help_text='The image of the achivement', null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='AchivementTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='achivements.achivement')),
            ],
            options={
                'verbose_name': 'achivement Translation',
                'db_table': 'achivements_achivement_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
