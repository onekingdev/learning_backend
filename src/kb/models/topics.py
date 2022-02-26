from django.db import models
from django.contrib import admin
from ..managers.topics import TopicManager
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class Topic(
        TimestampModel,
        RandomSlugModel,
        IsActiveModel,
        MPTTModel,
        TranslatableModel):
    PREFIX = 'topic_'

    translations = TranslatedFields(
        name=models.CharField(max_length=256)
    )

    area_of_knowledge = models.ForeignKey(
        'kb.AreaOfKnowledge',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='sub_topics'
    )
    # universal_topic = models.ManyToManyField(
    #     'universals.UniversalTopic',
    #     blank=True
    # )

    video_assistor = models.URLField(null=True, blank=True)

    objects = TopicManager()

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name or '')

        if self.parent:
            self.area_of_knowledge = self.parent.area_of_knowledge
        sup = super().save(*args, **kwargs)
        return sup


class TopicGrade(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'topic_grade_'

    grade = models.ForeignKey(
        'kb.Grade',
        on_delete=models.PROTECT,
    )
    topic = models.ForeignKey(
        'kb.Topic',
        on_delete=models.PROTECT,
    )
    standard_code = models.CharField(max_length=128, null=True, blank=True)

    @admin.display(description='Audience')
    def grade_audience(self):
        return self.grade.audience

    def __str__(self):
        return '{}/{}'.format(self.topic, self.grade)


class Prerequisite(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'prerequisite_'

    topic_grade = models.ForeignKey(
        TopicGrade, on_delete=models.PROTECT, related_name="Topic_grade")
    prerequisites = models.ManyToManyField(TopicGrade, blank=True)
    information = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}/{}'.format(self.topic_grade, self.prerequisite)
