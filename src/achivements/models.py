from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

class Achivement(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    hex_color = models.CharField(null=True, blank=True, max_length=16)
    name  = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(editable=False)
    image = models.TextField(null=True)
    level_required = models.ForeignKey('experiences.Level', on_delete=models.PROTECT, null=True, blank=True)
    engangement_points = models.IntegerField(null=True)
    coins_earned = models.IntegerField(null=True)


    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
