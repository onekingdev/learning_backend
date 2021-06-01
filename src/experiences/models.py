from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


# Create your models here.

class Level(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'lvl_'
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=128, null=True)
    points_required = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name