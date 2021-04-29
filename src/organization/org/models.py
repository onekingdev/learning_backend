from django.db import models
from django.utils.text import slugify
from addresses.models import Address
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel

# Create your models here.

class Organization(MPTTModel, TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'prs_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        type_of = models.CharField(max_length=128, null=True),
        slug = models.SlugField(editable=False)
    ),
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name+' '+self.last_name

class OrganizationPersonnel(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'prs_'
    user  = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    organization  = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)

    name  = models.CharField(max_length=128, null=True)
    last_name  = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=128, null=True)
    date_of_birth = models.DateField(null=True)
    identification_number = models.CharField(max_length=128, null=True)
    position = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name+' '+self.last_name

