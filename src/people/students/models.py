from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel
from kb.area_of_knowledges.models import AreaOfKnowledge

# Create your models here.

class Student(TimestampModel, UUIDModel):
    PREFIX = 'stdnt_'
    user  = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    # grade = models.ForeignKey('kb.Grade', on_delete=models.PROTECT, null=True)
    # first_name = models.CharField(max_length=64, null=True, blank=True)
    # last_name = models.CharField(max_length=64, null=True, blank=True)
    # dob = models.DateField(null=True, blank=True)
    # audience


    def get_completed_assessments_set(self):
        return self.assessment_set.filter(is_completed=True)

    def get_ongoin_assessments_set(self):
        return self.assessment_set.filter(is_completed=False)

    def get_pending_assessment_area_of_knowledge_set(self):
        return AreaOfKnowledge.objects.exclude(assessment__in=self.assessment_set.all())

    @property
    def get_full_name(self):
        return (self.first_name if self.first_name else ' ') + (self.last_name if self.last_name else ' ')

    def __str__(self):
        return self.get_full_name
