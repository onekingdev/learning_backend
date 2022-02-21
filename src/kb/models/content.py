from django.db import models
from django.contrib import admin
from ckeditor.fields import RichTextField
from polymorphic.models import PolymorphicModel
from kb.managers.content import QuestionManager
from gtts import gTTS

from django.utils.html import strip_tags

from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, IsActiveModel


class Question(
        TimestampModel,
        RandomSlugModel,
        IsActiveModel,
        TranslatableModel):
    PREFIX = 'question_'
    translations = TranslatedFields(
        question_text=RichTextField(blank=True)
    )
    topic = models.ForeignKey(
        'kb.Topic', on_delete=models.PROTECT)
    grade = models.ForeignKey(
        'kb.Grade', on_delete=models.PROTECT)
    objects = QuestionManager()
    def __str__(self):
        return strip_tags(self.safe_translation_getter("question_text", any_language=True))[:100]

    def __repr__(self):
        return strip_tags(self.safe_translation_getter("question_text", any_language=True))[:100]

    def get_questionimageasset_set(self):
        return QuestionImageAsset.objects.filter(question=self)

    def get_questionvideoasset_set(self):
        return QuestionVideoAsset.objects.filter(question=self)

    def get_questionaudioasset_set(self):
        return QuestionAudioAsset.objects.filter(question=self)
    
    def save_gtts(self):
        Text = self.safe_translation_getter("question_text", any_language=True)
        language = self.get_current_language()
        # TTS = gTTS(text=Text, lang=language)
        # TTS.save("media/gtts/question/" + self.random_slug + "_" + language + ".mp3")
    def save(self, *args, **kwargs):
        # self.set_calculated_fields()
        # ---------------- save gtts audio file -S-------------------#
        super().save(*args, **kwargs)
        self.save_gtts()
        # ---------------- save gtts audio file -E-------------------#

    @admin.display(description='Question')
    def question(self):
        return self.safe_translation_getter("question_text", any_language=True)

    @admin.display(description='Audience')
    def grade_audience(self):
        return self.grade.audience

    @admin.display(description='Topic identifier')
    def topic_identifier(self):
        return self.topic.identifier


class QuestionAsset(TimestampModel, RandomSlugModel, PolymorphicModel):

    class Meta:
        ordering = ['order']

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)

    @admin.display(description='Question identifier')
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
    audio_file = models.FileField()


class QuestionTTSAsset(QuestionAsset):
    PREFIX = 'question_tts_asset_'
    tts_file = models.FileField(null=True, blank=True)


class QuestionVideoAsset(QuestionAsset):
    PREFIX = 'question_video_asset_'
    url = models.URLField()


class AnswerOption(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'answer_option_'
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    translations = TranslatedFields(
        answer_text=models.CharField(max_length=256),
        explanation=RichTextField(null=True, blank=True),
        image=models.ImageField(null=True, blank=True),
        audio_file=models.FileField(null=True, blank=True),
        video=models.URLField(null=True, blank=True),
    )
    is_correct = models.BooleanField(default=False)
    def save_gtts(self):
        Text = self.safe_translation_getter("answer_text", any_language=True)
        language = self.get_current_language()
        # TTS = gTTS(text=Text, lang=language)
        # TTS.save("media/gtts/answer/" + self.random_slug + "_" + language + ".mp3")
    def save(self, *args, **kwargs):
        # ---------------- save gtts audio file -S-------------------#
        super().save(*args, **kwargs)
        self.save_gtts()
        # ---------------- save gtts audio file -E-------------------#
    def __str__(self):
        return self.safe_translation_getter("answer_text", any_language=True)
