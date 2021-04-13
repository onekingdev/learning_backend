from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

class AreaOfKnowledge(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'aok_'
    hex_color = models.CharField(null=True, blank=True, max_length=16)
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, unique=True),
        slug = models.SlugField(editable=False)
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
