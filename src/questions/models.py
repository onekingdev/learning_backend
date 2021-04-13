from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

class Question(TimestampModel, UUIDModel, TranslatableModel):
    PREFIX = 'qwstn_'
    translations = TranslatedFields(
        question_text = RichTextField(blank=True)
    )
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)

    def __str__(self):
        return self.question_text

    def get_questionimageasset_set(self):
        return QuestionImageAsset.objects.filter(question=self)

    def get_questionvideoasset_set(self):
        return QuestionVideoAsset.objects.filter(question=self)

    def get_questionaudioasset_set(self):
        return QuestionAudioAsset.objects.filter(question=self)

class QuestionAsset(TimestampModel, RandomSlugModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class QuestionImageAsset(QuestionAsset):
    image = models.ImageField()

class QuestionAudioAsset(QuestionAsset):
    audio_file = models.FileField()

class QuestionVideoAsset(QuestionAsset):
    url = models.URLField()