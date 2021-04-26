from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField

from kb.grades.models import Grade
from kb.area_of_knowledges.models import AreaOfKnowledge

from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel



# Create your models here.

class Group(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'grp_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        acronym = models.CharField(max_length=128, null=True),
        population = models.IntegerField(max_length=40, null=True)
    )

    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True, blank=True)
    area_of_knowledges = models.ManyToManyField(AreaOfKnowledge, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name