from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel, ActiveManager

# Create your models here.

class LevelManager(ActiveManager, TranslatableManager):
    pass

class Level(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'lvl_'
    
    translations = TranslatedFields(
    	name  = models.CharField(max_length=128, null=True)
    )

    points_required = models.IntegerField(null=True)

    objects = LevelManager()