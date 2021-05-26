from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


# Create your models here.

class Group(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'grp_'
    id = models.AutoField(primary_key=True)
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        internal_code = models.CharField(max_length=128, null=True),
        population = models.IntegerField(max_length=40, null=True)
    )

    grade = models.ForeignKey('kb.Grade', on_delete=models.PROTECT, null=True, blank=True)
    area_of_knowledges = models.ManyToManyField('kb.AreaOfKnowledge', blank=True)

    def __str__(self):
        return self.name

class School(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'sch_'
    id = models.AutoField(primary_key=True)
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        slug = models.SlugField(editable=False),
        internal_code = models.CharField(max_length=128, null=True),
        type_of = models.CharField(max_length=100, null=True)
    )

    student_plan = models.ManyToManyField('kb.StudentPlan', blank=True)
    organization =  models.ForeignKey('organization.Organization', blank=True)
    teacher =  models.ManyToManyField('organization.Teacher', blank=True)
    student =  models.ManyToManyField('students.Student', blank=True)
    group =  models.ManyToManyField('organization.Group', blank=True)

    def __str__(self):
        return self.name

class SchoolPersonnel(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'prs_'
    id = models.AutoField(primary_key=True)
    user  = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
    school  = models.ForeignKey('organization.School', on_delete=models.PROTECT, null=True)

    name  = models.CharField(max_length=128, null=True)
    last_name  = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=128, null=True)
    date_of_birth = models.DateField(null=True)
    identification_number = models.CharField(max_length=128, null=True)
    position = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name+' '+self.last_name


class AdministrativePersonnel(SchoolPersonnel):
    pass

class Teacher(SchoolPersonnel):
    pass
