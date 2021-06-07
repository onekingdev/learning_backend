from django.db import models
from ..managers.topics import TopicManager
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, IsActiveModel, UUIDModel

class Topic(TimestampModel, RandomSlugModel, IsActiveModel, MPTTModel, TranslatableModel):
    PREFIX = 'unv_tpic_'
    
    name  = models.CharField(max_length=128)
    slug = models.SlugField(editable=False)
    area_of_knowledge = models.ForeignKey('universals.AreaOfKnowledge', on_delete=models.PROTECT, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_topics')
    standard_code  = models.CharField(max_length=128, null=True, blank=True)

    objects = TopicManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.parent:
            self.area_of_knowledge = self.parent.area_of_knowledge
        sup = super().save(*args, **kwargs)
        return sup