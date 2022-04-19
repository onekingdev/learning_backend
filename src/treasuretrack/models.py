from django.db import models
from django.core.validators import MinValueValidator
from app.models import IsActiveModel


class DailyTreasureLevel(IsActiveModel):
    name = models.CharField(max_length=128)
    level = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(1)]
    )
    coins_required = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ['level']


class DailyTreasure(IsActiveModel):
    level = models.ForeignKey(DailyTreasureLevel, on_delete=models.PROTECT)
    coins_awarded = models.PositiveIntegerField(blank=True, null=True)
    collectibles_awarded = models.ManyToManyField('collectibles.Collectible')
