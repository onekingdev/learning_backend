from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields
from .managers import TopicManager
from django.utils.text import slugify

class Topic(TimestampModel, RandomSlugModel, MPTTModel, TranslatableModel):
    PREFIX = 'tpic_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128)
    )
    area_of_knowledge = models.ForeignKey(AreaOfKnowledge, on_delete=models.PROTECT, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,)
    standard_code  = models.CharField(max_length=128, null=True, blank=True)

    objects = TopicManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.area_of_knowledge = self.parent.area_of_knowledge
        sup = super().save(*args, **kwargs)
        return sup
