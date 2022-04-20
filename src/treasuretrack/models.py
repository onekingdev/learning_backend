from django.db import models
from django.core.validators import MinValueValidator
from app.models import IsActiveModel, TimestampModel
from wallets.models import Deposit


class DailyTreasureLevel(IsActiveModel):
    name = models.CharField(max_length=128)
    level = models.PositiveIntegerField(
        unique=True,
    )
    coins_required = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ['level']

    def get_next_level(self):
        pass


class DailyTreasure(IsActiveModel):
    level = models.ForeignKey(DailyTreasureLevel, on_delete=models.PROTECT)
    coins_awarded = models.PositiveIntegerField(blank=True, null=True)
    collectibles_awarded = models.ManyToManyField('collectibles.Collectible')


class StudentDailyTreasure(TimestampModel):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    daily_treasure = models.ForeignKey(DailyTreasure, on_delete=models.CASCADE)


class DailyTreasureTransaction(Deposit):
    daily_treasure = models.ForeignKey(
        StudentDailyTreasure,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = self.daily_treasure.coins_awarded
            self.comment = "Daiy Treasure Coins"
            # if not self.coins_awarded:
            #     self.amount = 0
            # if self.collectibles_awarded:
            #     for collectible in self.collectibles_awarded.all():
            #         student_collectible, new = StudentCollectible.objects.get_or_create(
            #             student=self.account.user.student,
            #             collectible=collectible,
            #         )
            #         if not new:
            #             student_collectible.amount += 1
            #         student_collectible.save()
            #     self.comment = "Daiy Treasure Collectible"
            # if self.coins_awarded and self.collectibles_awarded:
            #     self.comment = "Daiy Treasure Coins & Collectible"
        super().save(*args, **kwargs)
