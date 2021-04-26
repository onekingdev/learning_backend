from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

# Create your models here.

class Address(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'prs_'
    translations = TranslatedFields(
        street  = models.CharField(max_length=128, null=True),
        ext_no  = models.CharField(max_length=20, null=True),
        int_no = models.CharField(max_length=20, null=True),
        city = models.CharField(max_length=50, null=True),
        zip = models.CharField(max_length=20, null=True),
        state = models.CharField(max_length=50,null=True),
        country = models.CharField(max_length=128, null=True),
        type = models.CharField(max_length=128, null=True)
    )

    def __str__(self):
        return self.street+' '+self.ext_no+' '+self.city+', '+self.zip+' '+self.state+' '+self.country