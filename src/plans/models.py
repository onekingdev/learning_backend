from django.db import models
from django.utils.text import slugify
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class StudentPlan(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'student_plan_'

    name = models.CharField(max_length=128)
    slug = models.SlugField(editable=False)
    total_credits = models.IntegerField(null=True)
    validity_date = models.DateTimeField(null=True)
    audience = models.ForeignKey(
        'audiences.Audience',
        on_delete=models.PROTECT,
        null=True,
        blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class StudentPlanTopicGrade(TimestampModel, UUIDModel, IsActiveModel):

    question = models.ManyToManyField('content.Question')
    topic_grade = models.ForeignKey(
        'kb.TopicGrade',
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    student_plan = models.ForeignKey(
        'plans.StudentPlan',
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    credit_value = models.IntegerField(null=True)
    is_aproved = models.IntegerField(null=True)
    is_failed = models.IntegerField(null=True)
