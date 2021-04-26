from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify


# Create your models here.

class Parent(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'prnt_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        last_name  = models.CharField(max_length=128, null=True),
        gender = models.CharField(max_length=128, null=True),
        age = models.IntegerField(max_length=3, null=True)
    )

    def __str__(self):
        return self.name+' '+self.last_name