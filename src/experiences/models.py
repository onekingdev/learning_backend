from django.db import models
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from app.models import RandomSlugModel, TimestampModel, IsActiveModel, ActiveManager


class LevelManager(ActiveManager, TranslatableManager):
    pass


class Level(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'level_'

    translations = TranslatedFields(
        name=models.CharField(max_length=128, null=True)
    )

    points_required = models.IntegerField(null=True)

    objects = LevelManager()
