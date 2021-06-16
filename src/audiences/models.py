from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel, ActiveManager
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from django.utils.text import slugify


class AudienceManager(ActiveManager, TranslatableManager):
    pass

class Audience(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'au_'
    
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, unique=True)
    )
    slug = models.SlugField(editable=False)
    
    objects = AudienceManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
