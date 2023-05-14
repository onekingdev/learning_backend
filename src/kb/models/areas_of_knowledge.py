from django.db import models
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel


class AreaOfKnowledge(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'aok_'

    translations = TranslatedFields(
        name=models.CharField(max_length=128, unique=True)
    )

    hex_color = models.CharField(null=True, blank=True, max_length=16)
    slug = models.SlugField(editable=False)
    image = models.ImageField(null=True, blank=True,
                              help_text='The image of the island')

    audience = models.ForeignKey(
        'audiences.Audience', on_delete=models.PROTECT, null=True, blank=True)
    universal_area_knowledge = models.ForeignKey(
        'universals.UniversalAreaOfKnowledge', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
