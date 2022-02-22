from django.db import models
from app.models import RandomSlugModel, TimestampModel,IsActiveModel
from wallets.models import Withdraw


class Game(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'game_'

    name = models.CharField(max_length=64, null=True, blank=True)
    image = models.URLField(null=True)
    cost = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=15)
    play_stats = models.BigIntegerField(default=0, null=True)
    category = models.ForeignKey(
        'games.GameCategory', on_delete=models.PROTECT, null=True, blank=True)
    

class GameCategory(TimestampModel, RandomSlugModel, IsActiveModel):
    name = models.CharField(max_length=25, null=True)
    image = models.URLField(null=True)


class PlayGameTransaction(Withdraw):
    game = models.ForeignKey(
        Game, on_delete=models.PROTECT, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = self.game.cost
        return super().save(*args, **kwargs)