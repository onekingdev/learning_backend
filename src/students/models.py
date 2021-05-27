from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

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
    id = models.AutoField(primary_key=True)
    user  = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    age = models.IntegerField(null=True)

    student_plan = models.ManyToManyField('kb.StudentPlan')
    group =  models.ManyToManyField('organization.Group',blank=True)

    class Meta:
        ordering = ['last_name']

    @property
    def get_full_name(self):
        return (self.first_name if self.first_name else ' ') + (self.last_name if self.last_name else ' ')

    def __str__(self):
        return self.get_full_name

# Create your models here.
class Avatar(TimestampModel, UUIDModel, IsActiveModel):
    TYPE_COMPLETE = 'Completo'
    TYPE_TOP = 'Head'
    TYPE_MIDDLE = 'Body'
    TYPE_BOTTOM = 'Legs'
    TYPE_CHOICES = (
        (TYPE_COMPLETE, 'C'),
        (TYPE_TOP, 'H'),
        (TYPE_MIDDLE, 'B'),
        (TYPE_BOTTOM, 'L')
    )

    PREFIX = 'avt_'
    id = models.AutoField(primary_key=True)
    type_of = models.CharField(max_length=25, null=True, choices=TYPE_CHOICES)
    student  = models.ForeignKey('students.Student', on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    path = models.TextField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']

##
##class StudentTopicMastery():
  ##  student
    ##topic
    ##block
    ##timestamp mastery
    # TODO: pensar bien com ohacer esto... quz'as valga la pena abstraer no solo el mastery sino toda la "transaccion" de los topics para un estudiante
