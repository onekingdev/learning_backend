import os
from django.db import models
from django.contrib import admin
from ckeditor.fields import RichTextField
from polymorphic.models import PolymorphicModel
from kb.managers.content import (
    QuestionManager, AnswerOptionManager
)
from gtts import gTTS
from django.utils.html import strip_tags
from django.conf import settings
from pathlib import Path

from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, IsActiveModel


class Question(
        TimestampModel,
        RandomSlugModel,
        IsActiveModel,
        TranslatableModel):

    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'MC', 'Multiple Choice'
        MULTIPLE_SELECT = 'MS', 'Multiple Select'
        ORDER = 'O', 'Order'
        RELATE = 'R', 'Relate'
        TYPE_IN = 'T', 'Type In'

    PREFIX = 'question_'
    translations = TranslatedFields(
        question_text=RichTextField(blank=True)
    )
    topic = models.ForeignKey(
        'kb.Topic', on_delete=models.PROTECT)
    grade = models.ForeignKey(
        'kb.Grade', on_delete=models.PROTECT)
    objects = QuestionManager()
    question_type = models.CharField(
        max_length=2,
        choices=QuestionType.choices,
    )

    def __str__(self):
        return strip_tags(
            self.safe_translation_getter(
                "question_text",
                any_language=True
            )
        )[:100]

    def __repr__(self):
        return strip_tags(
            self.safe_translation_getter(
                "question_text",
                any_language=True
            )
        )[:100]

    def get_questionimageasset_set(self):
        return QuestionImageAsset.objects.filter(question=self)

    def get_questionvideoasset_set(self):
        return QuestionVideoAsset.objects.filter(question=self)

    def get_questionaudioasset_set(self):
        return QuestionAudioAsset.objects.filter(question=self)

    def get_questionttsasset(self):
        return QuestionTTSAsset.objects.get(question=self)

    def save_gtts(self):
        question_text = self.safe_translation_getter(
            "question_text", any_language=True)
        if not question_text:
            return None

        language = self.get_current_language()

        question_tts_asset, new = QuestionTTSAsset.objects.get_or_create(
            question=self,
        )

        try:
            tts_file = question_tts_asset.tts_file.file
        except Exception as e:
            tts_file = None
            print(e)

        if new or (tts_file is None):
            question_path = os.path.join(
                settings.MEDIA_ROOT, f'tts/{language}/{self.identifier}/')

            Path(question_path).mkdir(parents=True, exist_ok=True)

            tts_file_name = f'{self.identifier}.mp3'

            tts_file_path = os.path.join(question_path, tts_file_name)

            with open(tts_file_path, 'wb') as f:
                try:
                    tts = gTTS(text=question_text, lang=language)
                    tts.write_to_fp(f)
                except Exception as e:
                    print("Exception on gtts", e)

            question_tts_asset.tts_file = f'tts/{language}/{self.identifier}/{self.identifier}.mp3'
            question_tts_asset.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @ admin.display(description='Question')
    def question(self):
        return self.safe_translation_getter("question_text", any_language=True)

    @ admin.display(description='Audience')
    def grade_audience(self):
        return self.grade.audience

    @ admin.display(description='Topic identifier')
    def topic_identifier(self):
        return self.topic.identifier


class QuestionAsset(TimestampModel, RandomSlugModel, PolymorphicModel):

    class Meta:
        ordering = ['order']

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)

    @ admin.display(description='Question identifier')
    def question_slug(self):
        return self.question.random_slug

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = QuestionAsset.objects.filter(
                question=self.question).count() + 1
        return super().save(*args, **kwargs)


class QuestionImageAsset(QuestionAsset):
    PREFIX = 'question_image_asset_'
    image = models.URLField()


class QuestionAudioAsset(QuestionAsset):
    PREFIX = 'question_audio_asset_'
    # audio_file = models.FileField()
    audio_file = models.URLField(null=True)


class QuestionTTSAsset(QuestionAsset):
    PREFIX = 'question_tts_asset_'
    tts_file = models.FileField(null=True, blank=True, upload_to='tts')


class QuestionVideoAsset(QuestionAsset):
    PREFIX = 'question_video_asset_'
    url = models.URLField()


class AnswerOption(
    TimestampModel,
    RandomSlugModel,
    TranslatableModel,
    PolymorphicModel
):
    PREFIX = 'answer_option_'
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    is_correct = models.BooleanField(default=False)

    objects = AnswerOptionManager()

    @admin.display(description='Question type')
    def question_type(self):
        return self.question.question_type

    @admin.display(description='Answer')
    def answer_display(self):
        return self.__str__

    def save_gtts(self):
        answer_text = self.safe_translation_getter(
            "answer_text", any_language=True)
        if not answer_text:
            return None

        language = self.get_current_language()

        try:
            tts_file = self.tts_file.file
        except Exception as e:
            tts_file = None
            print(e)

        if tts_file is None:
            answer_path = os.path.join(
                settings.MEDIA_ROOT, f'tts/{language}/{self.question.identifier}/')

            Path(answer_path).mkdir(parents=True, exist_ok=True)

            tts_file_name = f'{self.identifier}.mp3'

            tts_file_path = os.path.join(answer_path, tts_file_name)

            with open(tts_file_path, 'wb') as f:
                try:
                    tts = gTTS(text=answer_text, lang=language)
                    tts.write_to_fp(f)
                except Exception as e:
                    print("Exception on gtts", e)

            self.tts_file = f'tts/{language}/{self.question.identifier}/{self.identifier}.mp3'
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class MultipleChoiceAnswerOption(AnswerOption):
    translations = TranslatedFields(
        answer_text=models.CharField(max_length=256),
        explanation=RichTextField(null=True, blank=True),
        image=models.URLField(null=True, blank=True),
        audio_file=models.URLField(null=True, blank=True),
        video=models.URLField(null=True, blank=True),
    )

    def __str__(self):
        return self.safe_translation_getter("answer_text", any_language=True)


class MultipleSelectAnswerOption(AnswerOption):
    translations = TranslatedFields(
        answer_text=models.CharField(max_length=256),
        explanation=RichTextField(null=True, blank=True),
        image=models.URLField(null=True, blank=True),
        audio_file=models.URLField(null=True, blank=True),
        video=models.URLField(null=True, blank=True),
    )

    def __str__(self):
        return self.safe_translation_getter("answer_text", any_language=True)


class TypeInAnswerOption(AnswerOption):
    translations = TranslatedFields(
        answer_text=models.CharField(max_length=256),
        explanation=RichTextField(null=True, blank=True),
        image=models.URLField(null=True, blank=True),
        audio_file=models.URLField(null=True, blank=True),
        video=models.URLField(null=True, blank=True),
    )

    def __str__(self):
        return self.safe_translation_getter("answer_text", any_language=True)


class OrderAnswerOption(AnswerOption):
    translations = TranslatedFields(
        answer_text=models.CharField(max_length=256),
        image=models.URLField(null=True, blank=True),
        audio_file=models.URLField(null=True, blank=True),
        video=models.URLField(null=True, blank=True),
    )
    order = models.IntegerField()

    def __str__(self):
        return self.safe_translation_getter("answer_text", any_language=True)


class RelateAnswerOption(AnswerOption):
    translations = TranslatedFields(
        key=models.CharField(max_length=256),
        value=models.CharField(max_length=256),
        key_image=models.URLField(null=True, blank=True),
        value_image=models.URLField(null=True, blank=True),
    )

    def __str__(self):
        return (
            self.safe_translation_getter("key", any_language=True)
            + " - "
            + self.safe_translation_getter("value", any_language=True)
        )
