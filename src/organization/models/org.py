from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

# Create your models here.

class Organization(MPTTModel, TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'prs_'
    
    name  = models.CharField(max_length=128, null=True)
    type_of = models.CharField(max_length=128, null=True)
    slug = models.SlugField(editable=False)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    student_plan = models.ManyToManyField('plans.StudentPlan')
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name+' '+self.last_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class OrganizationPersonnel(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'prs_'
    
    user  = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
    organization  = models.ForeignKey('organization.Organization', on_delete=models.PROTECT, null=True)

    name  = models.CharField(max_length=128, null=True)
    last_name  = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=128, null=True)
    date_of_birth = models.DateField(null=True)
    identification_number = models.CharField(max_length=128, null=True)
    position = models.CharField(max_length=128, null=True)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.name+' '+self.last_name
