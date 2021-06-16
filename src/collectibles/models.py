from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel, ActiveManager


# Create your models here.
class CollectibleCategoryManager(ActiveManager, TranslatableManager):
    pass

class CollectibleManager(ActiveManager, TranslatableManager):
    pass


class CollectibleCategory(TimestampModel, MPTTModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        description = models.TextField(null=True)
    )

    slug = models.CharField(max_length=128, null=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_categories')

    objects = CollectibleCategoryManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Collectible(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        description = models.TextField(null=True)
    )

    slug = models.CharField(max_length=128, null=True)
    price = models.FloatField(blank=True, null=True)
    category =  models.ForeignKey('collectibles.CollectibleCategory', on_delete=models.PROTECT, null=True, blank=True)
   
    objects = CollectibleManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class StudentTransactionCollectible(TimestampModel, RandomSlugModel, IsActiveModel):

    price =  models.FloatField(blank=True, null=True)
    purchase_date =  models.DateTimeField(null=True)
    collectible =  models.ForeignKey('collectibles.Collectible',null=True, on_delete=models.PROTECT, blank=True)
    movement =  models.ForeignKey('wallets.Transaction',null=True, on_delete=models.PROTECT, blank=True)
    student =  models.ForeignKey('students.Student',null=True, on_delete=models.PROTECT, blank=True)

    class Meta:
        ordering = ['create_timestamp']