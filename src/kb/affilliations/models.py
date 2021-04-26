from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify
from kb.grades.models import Grade

class Affilliation(TimestampModel, UUIDModel, TranslatableModel):
    PREFIX = 'affi_'
    translations = TranslatedFields(
        affilliation = models.CharField(max_length=256),
        slug = models.SlugField(editable=False)
    )
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)

    def __str__(self):
    	return self.affilliation