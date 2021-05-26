from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

# Create your models here.

class Grade(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'gde_'
    id = models.AutoField(primary_key=True)
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, null=True),
        slug = models.SlugField(editable=False)
    )

    audience = models.ForeignKey('audiences.Audience', on_delete=models.PROTECT)

    def __str__(self):
        return self.name