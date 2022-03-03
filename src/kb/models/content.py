from django.db import models
from django.contrib import admin
from ckeditor.fields import RichTextField
from polymorphic.models import PolymorphicModel
from kb.managers.content import QuestionManager
from gtts import gTTS
import os
from django.utils.html import strip_tags

from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, IsActiveModel
import time

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
    
    # ---------------- Generate gtts audio file -S-------------------#
    def save_gtts(self):
        # get question's text
        text = self.safe_translation_getter("question_text", any_language=True)
        if not text: return
        # get language of current question
        language = self.get_current_language()

        #------------- generate path to save gtts and save text to speech audio file to the path-S-------------#
        path = "media/gtts/" + language  + "/" + self.identifier
        isPathExist = os.path.exists(path)
        if not isPathExist:
            os.makedirs(path)
        if not isPathExist:
                os.makedirs(path)
        try:
            TTS = gTTS(text=text, lang=language)
            time.sleep(1)
            TTS.save(path + "/question" + ".mp3")
        except Exception as e:
            print("Exception on gtts", e)
        #------------- generate path to save gtts and save text to speech audio file to the path-E-------------#
    # ---------------- Generate gtts audio file -E-------------------#

    def save(self, *args, **kwargs):
        # self.set_calculated_fields()
        super().save(*args, **kwargs)
        self.save_gtts()

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
    # audio_file = models.FileField()
    audio_file = models.URLField(null=True)


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

    # ---------------- Generate gtts audio file -S-------------------#
    def save_gtts(self):
        text = self.safe_translation_getter("answer_text", any_language=True)
        # if text is empty or answer's question is empty, disable to save
        if not text: return
        if not self.question : return

        # get current answer's language
        language = self.get_current_language()

        #------------- generate path to save gtts and save text to speech audio file to the path-S-------------#
        path = "media/gtts/" + language + "/" + self.question.identifier
        isPathExist = os.path.exists(path)
        if not isPathExist:
            os.makedirs(path)
        try:
            TTS = gTTS(text=text, lang=language)
            time.sleep(1)
            TTS.save(path +"/answer_" + self.random_slug + ".mp3")
        except Exception as e:
            print("Exception on gtts", e)
        #------------- generate path to save gtts and save text to speech audio file to the path -E-------------#
    # ---------------- Generate gtts audio file -E-------------------#

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_gtts()

    def __str__(self):
        return self.safe_translation_getter("answer_text", any_language=True)
