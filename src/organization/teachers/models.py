from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from organization.groups.models import Group
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel


# Create your models here.

class Teacher(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'tch_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        last_name  = models.CharField(max_length=128, null=True),
        gender = models.CharField(max_length=128, null=True),
        age = models.IntegerField(max_length=3, null=True),
        contract_date = models.DateField(null=True),
        identification_number = models.CharField(max_length=128, null=True),
        position = models.CharField(max_length=128, null=True)
    )
    user  = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name+' '+self.last_name

class GroupTeacher(TimestampModel, RandomSlugModel):
	PREFIX = "grp_tch_"
	group =  models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True)
	teacher =  models.ManyToManyField(Teacher, on_delete=models.PROTECT, null=True, blank=True)