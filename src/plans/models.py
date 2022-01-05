from django.db import models
from django.utils.text import slugify
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class StudentPlan(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'student_plan_'

    name = models.CharField(max_length=128)
    slug = models.SlugField(editable=False)
    audience = models.ForeignKey(
        'audiences.Audience',
        on_delete=models.PROTECT,
    )
    topic_grade = models.ManyToManyField(
        'kb.TopicGrade',
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
