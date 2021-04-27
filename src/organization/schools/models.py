from django.db import models
from django.utils.text import slugify

from addresses.models import Address
from people.students.models import Student
from organization.groups.models import Group
from organization.teachers.models import Teacher
from organization.org.models import Organization
from organization.personnels.models import Personnel

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


# Create your models here.

class School(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'sch_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        slug = models.SlugField(editable=False),
        acronym = models.CharField(max_length=128, null=True),
        foundation_date = models.DateTimeField(null=True),
        population = models.IntegerField(max_length=20, null=True),
        open_hour = models.TimeField(max_length=50, null=True),
        close_hour = models.TimeField(max_length=50, null=True),
        type = models.CharField(max_length=100, null=True)
    )

    organization =  models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True)
	address =  models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
	teacher =  models.ManyToManyField(Teacher, on_delete=models.PROTECT, null=True, blank=True)
	student =  models.ManyToManyField(Student, on_delete=models.PROTECT, null=True, blank=True)
	group =  models.ManyToManyField(Group, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name
	