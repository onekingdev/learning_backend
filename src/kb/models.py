from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from .managers import TopicManager
from django.utils.text import slugify


# Create your models here.
"""
class Grade(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'gde_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True)
    )

"""

class AreaOfKnowledge(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'aok_'
    hex_color = models.CharField(null=True, blank=True, max_length=16)
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, unique=True),
        slug = models.SlugField(editable=False)
    )


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Topic(TimestampModel, RandomSlugModel, MPTTModel, TranslatableModel):
    PREFIX = 'tpic_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128)
    )
    area_of_knowledge = models.ForeignKey(AreaOfKnowledge, on_delete=models.PROTECT, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,)
    standard_code  = models.CharField(max_length=128, null=True, blank=True)

    objects = TopicManager()

    def save(self, *args, **kwargs):
        if self.parent:
            self.area_of_knowledge = self.parent.area_of_knowledge
        sup = super().save(*args, **kwargs)
        return sup


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


class AnswerOption(TimestampModel, UUIDModel, TranslatableModel):
    PREFIX = 'answopt_'
    translations = TranslatedFields(
        answer_text = models.CharField(max_length=256),
        explanation = RichTextField(blank=True,)
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)



