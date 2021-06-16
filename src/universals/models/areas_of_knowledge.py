from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

class UniversalAreaOfKnowledge(TimestampModel, RandomSlugModel, IsActiveModel,TranslatableModel):
    PREFIX = 'unv_aok_'
    
    name  = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
