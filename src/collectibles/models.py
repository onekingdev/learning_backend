from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel


# Create your models here.

class CollectibleCategory(TimestampModel, MPTTModel, RandomSlugModel, IsActiveModel):
    
    name  = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    slug = models.CharField(max_length=128, null=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_categories')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Collectible(TimestampModel, RandomSlugModel, IsActiveModel):
    
    name  = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)
    slug = models.CharField(max_length=128, null=True)
    price = models.FloatField(blank=True, null=True)
    category =  models.ForeignKey('collectibles.CollectibleCategory', on_delete=models.PROTECT, null=True, blank=True)
   
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class StudentTransactionCollectible(TimestampModel, RandomSlugModel, IsActiveModel):
    
    name  = models.CharField(max_length=128, null=True)
    price =  models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(null=True)
    collectible =  models.ForeignKey('collectibles.Collectible',null=True, on_delete=models.PROTECT, blank=True)
    movement =  models.ForeignKey('wallets.Transaction',null=True, on_delete=models.PROTECT, blank=True)
    student =  models.ForeignKey('students.Student',null=True, on_delete=models.PROTECT, blank=True)

    class Meta:
        ordering = ['create_timestamp']