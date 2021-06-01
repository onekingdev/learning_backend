from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel


class AreaOfKnowledge(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'aok_'
    id = models.AutoField(primary_key=True)
    hex_color = models.CharField(null=True, blank=True, max_length=16)
    name  = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(editable=False)
    

    audience = models.ForeignKey('audiences.Audience', on_delete=models.PROTECT, null=True, blank=True)
    universal_area_knowledge = models.ForeignKey('universals.AreaOfKnowledge', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
