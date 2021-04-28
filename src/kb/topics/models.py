from django.db import models
from .managers import TopicManager
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from kb.area_of_knowledges.models import AreaOfKnowledge
from universal.topics.models import Topic as UniversalTopic
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel


class Topic(TimestampModel, RandomSlugModel, MPTTModel, TranslatableModel):
    PREFIX = 'tpic_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128)
    )
    area_of_knowledge = models.ForeignKey(AreaOfKnowledge, on_delete=models.PROTECT, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    universal_topic = models.ForeignKey(UniversalTopic, on_delete=models.PROTECT, null=True, blank=True)
    # TODO: univ topic debe ser m2m para que se puedan hacer los arboles como deba ser en casda caso
    # TODO: falta meter la audiencia de esto... quizas audienca debe ser un modelo abstracto
    # prerequisites = models.ManyToManyField(

    objects = TopicManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.area_of_knowledge = self.parent.area_of_knowledge
        sup = super().save(*args, **kwargs)
        return sup


class TopicGrade(TimestampModel, UUIDModel):
    PREFIX = 'tpic_grde_'
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    standard_code  = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
    	return '{}/{}'.format(self.topic, self.grade)
