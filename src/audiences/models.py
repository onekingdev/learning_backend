from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from parler.models import TranslatableModel, TranslatedFields
from .managers import TopicManager
from django.utils.text import slugify



# Create your models here.



class Audience(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'aok_'
    hex_color = models.CharField(null=True, blank=True, max_length=16)
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, unique=True),
        slug = models.SlugField(editable=False)
    )


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


