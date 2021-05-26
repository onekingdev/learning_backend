from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


# Create your models here.

class Guardian(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'grdn_'
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=128, null=True),
    last_name  = models.CharField(max_length=128, null=True),
    gender = models.CharField(max_length=128, null=True),
    user  = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name+' '+self.last_name

class GuardianStudent(TimestampModel, RandomSlugModel):
    PREFIX = "prnt_stnd_"
    id = models.AutoField(primary_key=True)
    guardian =  models.ForeignKey('guardians.Guardian', on_delete=models.PROTECT, null=True, blank=True)
    student =  models.ForeignKey('students.Student', on_delete=models.PROTECT, null=True, blank=True)
