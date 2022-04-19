from django.db import models
from django.core.validators import MinValueValidator
from app.models import IsActiveModel
from accounting.models import Account


class DailyTreasureLevel(IsActiveModel):
    level = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    coins_required = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )


class DailyTreasure(IsActiveModel):
    level = models.ForeignKey(DailyTreasureLevel, on_delete=models.PROTECT)
    coins_awarded = models.PositiveIntegerField(blank=True, null=True)
    collectibles_awarded = models.ManyToManyField('collectibles.Collectible')
