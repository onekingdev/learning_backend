from django.db import models

from .managers import TopicManager
from django.utils.text import slugify
from audiences.models import Audience
from students.models import Student
from organization.schools.models import School
from organization.org.models import Organization


from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from kb.area_of_knowledges.models import AreaOfKnowledge
from kb.grades.models import Grade
from universal.topics.models import Topic as UniversalTopic
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


class StudentPlan(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'std_pln_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128)
    )

    """
    total_credits 
    validity_date
    """
    audience = models.ManyToManyField(Audience, on_delete=models.PROTECT, null=True, blank=True)
    student = models.ManyToManyField(Student, on_delete=models.PROTECT, null=True, blank=True)
    school = models.ManyToManyField(School, on_delete=models.PROTECT, null=True, blank=True)
    organization = models.ManyToManyField(Organization, on_delete=models.PROTECT, null=True, blank=True)
    
    # TODO: falta meter la audiencia de esto... quizas audienca debe ser un modelo abstracto
   
    def __str__(self):
        return self.name

    def get_topics(self):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(id) FROM tpic_std_pln WHERE student_plan_id = %s",
            (self.id,)
        )
        value = cursor.fetchone()[0]
        if value is None:
            value = Decimal('0.0')
        return value

class Topic(TimestampModel, RandomSlugModel, IsActiveModel, MPTTModel, TranslatableModel):
    PREFIX = 'tpic_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128)
    )

    audience = models.ForeignKey(Audience, on_delete=models.PROTECT, null=True, blank=True)
    area_of_knowledge = models.ForeignKey(AreaOfKnowledge, on_delete=models.PROTECT, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    universal_topic = models.ManyToManyField(UniversalTopic, on_delete=models.PROTECT, null=True, blank=True)
    
    # TODO: falta meter la audiencia de esto... quizas audienca debe ser un modelo abstracto
    objects = TopicManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.area_of_knowledge = self.parent.area_of_knowledge
        sup = super().save(*args, **kwargs)
        return sup


class TopicGrade(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'tpic_grde_'
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, null=True, blank=True)
    standard_code  = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
    	return '{}/{}'.format(self.topic, self.grade)

class StudentTopicGrade(TimestampModel, UUIDModel, IsActiveModel):
    topic_grade =  models.ForeignKey(TopicGrade, on_delete=models.PROTECT, null=True, blank=True)
    student_plan =  models.ForeignKey(StudentPlan, on_delete=models.PROTECT, null=True, blank=True)

    """
    credit_value
    is_aproved
    is_failed
    """


class Prerequisite(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'pre_'
    topic_grade = models.ManyToManyField(TopicGrade, on_delete=models.PROTECT)
    topic = models.ManyToManyField(Topic, on_delete=models.PROTECT)
    """
        information
        advance_percentage
        advance_minum
        needed_choices
    """

    def __str__(self):
        return '{}/{}'.format(self.topic, self.grade)
