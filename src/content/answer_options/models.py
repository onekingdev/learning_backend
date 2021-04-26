from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify
from cnt.questions.models import Question

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