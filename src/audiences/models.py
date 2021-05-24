from django.db import models
from kb.topics.models import StudentPlan
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

class Audience(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'au_'
    hex_color = models.CharField(null=True, blank=True, max_length=16)
    translations = TranslatedFields(
        name  = models.CharField(max_length=128, unique=True),
        slug = models.SlugField(editable=False)
    )

    student_plan = models.ManyToManyField(StudentPlan, on_delete=models.PROTECT, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name