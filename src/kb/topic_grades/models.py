from django.db import models
from kb.grades.models import Grade
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel

class TopicGrade(TimestampModel, UUIDModel, TranslatableModel):
    PREFIX = 'affi_'
    translations = TranslatedFields(
        year_point = models.CharField(max_length=256),
        slug = models.SlugField(editable=False)
    )
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)

    def __str__(self):
    	return self.year_point