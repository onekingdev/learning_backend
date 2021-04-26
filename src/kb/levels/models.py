from django.db import models
from grades.models import Grade
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from area_of_knowledges.models import AreaOfKnowledge
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


# Create your models here.

class Level(TimestampModel, RandomSlugModel, TranslatableModel):
    PREFIX = 'lvl_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        slug = models.SlugField(editable=False)
    )

    def __str__(self):
        return self.name

class LevelArea(TimestampModel, RandomSlugModel, MPTTModel):
    PREFIX = 'lvl_ar_'
    translations = TranslatedFields(
        nickname  = models.CharField(max_length=128, null=True)
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    area_of_knowledge = models.ForeignKey(AreaOfKnowledge, on_delete=models.CASCADE)
    experience = models.FloatField(null=True)
    next_to = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nickname

class LevelGrade(TimestampModel, RandomSlugModel, MPTTModel):
    PREFIX = 'lvl_grd_'
    translations = TranslatedFields(
        nickname  = models.CharField(max_length=128, null=True)
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    experience = models.FloatField(null=True)
    next_to = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nickname