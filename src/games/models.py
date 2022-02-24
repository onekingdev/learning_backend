from unicodedata import category
from django.db import models
from app.models import RandomSlugModel, TimestampModel, IsActiveModel, ActiveManager
from wallets.models import Withdraw
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager


class GameCategoryManager(ActiveManager, TranslatableManager):
    pass


class GameManager(ActiveManager, TranslatableManager):
    pass


class Game(TimestampModel, TranslatableModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'game_'

    translations = TranslatedFields(
        name=models.CharField(max_length=128, null=True)
    )
    image = models.URLField(null=True)
    cost = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=15)
    play_stats = models.BigIntegerField(default=0, null=True)
    category = models.ManyToManyField('games.GameCategory')
    objects = GameManager()

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)
    

class GameCategory(TimestampModel, TranslatableModel, RandomSlugModel, IsActiveModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=25, null=True)
    )
    image = models.URLField(null=True)
    bg_color = models.CharField(null=True, blank=True, max_length=16)
    objects = GameCategoryManager()

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True)


class PlayGameTransaction(Withdraw):
    game = models.ForeignKey(
        Game, on_delete=models.PROTECT, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = self.game.cost
        return super().save(*args, **kwargs)