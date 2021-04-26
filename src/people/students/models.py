from django.db import models
from kb.grades.models import Grade
from kb.levels.models import Level
from organization.groups.models import Group
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

# Create your models here.

class Student(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'stdnt_'
    user  = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=128, null=True)
    age = models.IntegerField(max_length=3, null=True)

    level =  models.ManyToManyField(Level, on_delete=models.PROTECT, null=True, blank=True)
    group =  models.ManyToManyField(Group, on_delete=models.PROTECT, null=True, blank=True)

    def get_completed_assessments_set(self):
        return self.assessment_set.filter(is_completed=True)

    def get_ongoin_assessments_set(self):
        return self.assessment_set.filter(is_completed=False)

    @property
    def get_full_name(self):
        return (self.first_name if self.first_name else ' ') + (self.last_name if self.last_name else ' ')

    def __str__(self):
        return self.get_full_name
