from django.db import models
from kb.grades.models import Grade
from kb.topics.models import StudentPlan
from organization.groups.models import Group
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

# Create your models here.

class Student(TimestampModel, UUIDModel, IsActiveModel):
    GENDER_MALE = 'Male'
    GENDER_FEMALE = 'Female'
    GENDER_OTHER = 'Other'
    GENDER_CHOICES = (
        (GENDER_MALE, 'M'),
        (GENDER_FEMALE, 'F'),
        (GENDER_OTHER, 'O'),
    )

    PREFIX = 'stdnt_'
    user  = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    age = models.IntegerField(max_length=3, null=True)

    student_plan = models.ManyToManyField('kb.topics.StudentPlan', null=True)
    group =  models.ManyToManyField('kb.grades.Group',  null=True, blank=True)


    @property
    def get_full_name(self):
        return (self.first_name if self.first_name else ' ') + (self.last_name if self.last_name else ' ')

    def __str__(self):
        return self.get_full_name

##
##class StudentTopicMastery():
  ##  student
    ##topic
    ##block
    ##timestamp mastery
    # TODO: pensar bien com ohacer esto... quz'as valga la pena abstraer no solo el mastery sino toda la "transaccion" de los topics para un estudiante
