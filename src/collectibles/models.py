from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

class CollectibleCategory(TimestampModel, RandomSlugModel, MPTTModel, IsActiveModel, TranslatableModel):
    PREFIX = 'col_cat_'
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=128, blank=True, null=True)
    description  = models.TextField()
    slug = models.SlugField(editable=False)

    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Collectible(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'col_'
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=128, blank=True, null=True)
    description  = models.TextField()
    slug = models.SlugField(editable=False)
    
    price = models.FloatField(null=True, blank=True)
    category  = models.ForeignKey('collectibles.CollectibleCategory', on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class StudentCollectible(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'stu_col_'
    id = models.AutoField(primary_key=True)
    collectible  = models.ForeignKey('collectibles.Collectible', on_delete=models.PROTECT, null=True)
    student  = models.ForeignKey('students.Student', on_delete=models.PROTECT, null=True)
    movement  = models.ForeignKey('wallets.Transaction', on_delete=models.PROTECT, null=True)
    price = models.FloatField(null=True, blank=True)
    purchase_date = models.DateTimeField(null=True)
