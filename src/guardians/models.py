from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


# Create your models here.

class Guardian(TimestampModel, RandomSlugModel, IsActiveModel):
    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDER_OTHER = 'OTHER'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )
    
    PREFIX = 'grdn_'
    
    name  = models.CharField(max_length=128, null=True)
    last_name  = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    user  = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name+' '+self.last_name

class GuardianStudent(TimestampModel, RandomSlugModel):
    PREFIX = "prnt_stnd_"
    
    guardian =  models.ForeignKey('guardians.Guardian', on_delete=models.PROTECT, null=True, blank=True)
    student =  models.ForeignKey('students.Student', on_delete=models.PROTECT, null=True, blank=True)
