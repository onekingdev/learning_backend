from django.db import models
from django.utils.text import slugify
from org.models import Organization
from addresses.models import Address
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel

# Create your models here.

class Personnel(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'prs_'
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        last_name  = models.CharField(max_length=128, null=True),
        gender = models.CharField(max_length=128, null=True),
        age = models.IntegerField(max_length=3, null=True),
        contract_date = models.DateField(null=True),
        identification_number = models.CharField(max_length=128, null=True),
        position = models.CharField(max_length=128, null=True)
    )

    def __str__(self):
        return self.name+' '+self.last_name

class PersonnelAddress(TimestampModel, RandomSlugModel):
	PREFIX = "prs_add_"
	personnel =  models.ForeignKey(Personnel, on_delete=models.PROTECT, null=True, blank=True)
	address =  models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)

class PersonnelOrganization(TimestampModel, RandomSlugModel):
	PREFIX = "prs_org_"
	personnel =  models.ForeignKey(Personnel, on_delete=models.PROTECT, null=True, blank=True)
	organization =  models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True)