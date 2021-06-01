from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class StudentPlan(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'std_pln_'
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=128)
    slug = models.SlugField(editable=False)
    total_credits = models.IntegerField(null=True)
    validity_date = models.DateTimeField(null=True)
    audience =  models.ForeignKey('audiences.Audience', on_delete=models.PROTECT, null=True, blank=True)
   
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_topics(self):
        # TODO: rehacer esto con Django ORM
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(id) FROM tpic_std_pln WHERE student_plan_id = %s",
            (self.id,)
        )
        value = cursor.fetchone()[0]
        if value is None:
            value = Decimal('0.0')
        return value

class StudentPlanTopicGrade(TimestampModel, UUIDModel, IsActiveModel):
    id = models.AutoField(primary_key=True)
    question = models.ManyToManyField('content.Question')
    topic_grade =  models.ForeignKey('kb.TopicGrade', on_delete=models.PROTECT, null=True, blank=True)
    student_plan =  models.ForeignKey('plans.StudentPlan', on_delete=models.PROTECT, null=True, blank=True)
    credit_value = models.IntegerField(null=True)
    is_aproved = models.IntegerField(null=True)
    is_failed = models.IntegerField(null=True)