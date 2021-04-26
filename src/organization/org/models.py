from django.db import models
from django.utils.text import slugify
from addresses.models import Address
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel

# Create your models here.

class Organization(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'prs_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        type = models.CharField(max_length=128, null=True),
        founders = models.CharField(max_length=128, null=True),
        date_foundation = models.DateTimeField(null=True),
        slug = models.SlugField(editable=False)
    ),
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name+' '+self.last_name

class OrganizationAddress(TimestampModel, RandomSlugModel):
    PREFIX = "org_add_"
    organization =  models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True)
    address =  models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)