from django.db import models
from django.utils.text import slugify

from students.models import Student
from organization.org.models import Organization

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


# Create your models here.

class Group(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'grp_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        internal_code = models.CharField(max_length=128, null=True),
        population = models.IntegerField(max_length=40, null=True)
    )

    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True, blank=True)
    area_of_knowledges = models.ManyToManyField(AreaOfKnowledge, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

class School(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'sch_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        slug = models.SlugField(editable=False),
        internal_code = models.CharField(max_length=128, null=True),
        type_of = models.CharField(max_length=100, null=True)
    )

    organization =  models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True)
	teacher =  models.ManyToManyField(Teacher, on_delete=models.PROTECT, null=True, blank=True)
	student =  models.ManyToManyField(Student, on_delete=models.PROTECT, null=True, blank=True)
	group =  models.ManyToManyField(Group, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

class SchoolPersonnel(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'prs_'
    user  = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    school  = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)

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
