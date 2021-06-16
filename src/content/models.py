from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from polymorphic.models import PolymorphicModel


from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class Question(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'question_'
    translations = TranslatedFields(
        question_text = RichTextField(blank=True)
    )
    topic = models.ForeignKey('universals.UniversalTopic', on_delete=models.PROTECT)
    topic_grade = models.ForeignKey('kb.TopicGrade', on_delete=models.PROTECT)

    def __str__(self):
        return self.question_text

    def get_questionimageasset_set(self):
        return QuestionImageAsset.objects.filter(question=self)

    def get_questionvideoasset_set(self):
        return QuestionVideoAsset.objects.filter(question=self)

    def get_questionaudioasset_set(self):
        return QuestionAudioAsset.objects.filter(question=self)


class QuestionAsset(TimestampModel, RandomSlugModel, PolymorphicModel):

    class Meta:
        ordering = ['order']

    PREFIX = 'question_asset_'
    question = models.ForeignKey('content.Question', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=10)


class QuestionImageAsset(QuestionAsset):
    image = models.ImageField()


class QuestionAudioAsset(QuestionAsset):
    audio_file = models.FileField()


class QuestionVideoAsset(QuestionAsset):
    url = models.URLField()


class AnswerOption(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'answer_option_'
    question = models.ForeignKey('content.Question', on_delete=models.PROTECT)
    translations = TranslatedFields(
        answer_text = models.CharField(max_length=256),
        explanation = RichTextField(null=True, blank=True), 
        image = models.ImageField(null=True, blank=True), 
        audio_file = models.FileField(null=True, blank=True), 
        video = models.URLField(null=True, blank=True),
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

