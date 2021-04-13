from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify


# Create your models here.

class Grade(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'gde_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True)
    )

    def __str__(self):
        return self.name