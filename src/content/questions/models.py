from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from kb.topics.models import TopicGrade
from universal.topics.models import Topic as UniversalTopic
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

class AnswerOption(TimestampModel, UUIDModel, TranslatableModel):
    PREFIX = 'answopt_'
    translations = TranslatedFields(
        answer_text = models.CharField(max_length=256),
        explanation = RichTextField(blank=True,)
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

class Question(TimestampModel, UUIDModel, IsActiveModel, TranslatableModel):
    PREFIX = 'qwstn_'
    translations = TranslatedFields(
        question_text = RichTextField(blank=True)
    )
    topic = models.ForeignKey(UniversalTopic, on_delete=models.PROTECT)
    topic_grade = models.ForeignKey(TopicGrade, on_delete=models.PROTECT)

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