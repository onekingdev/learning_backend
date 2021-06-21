from django.db import models
from accounting.models import Account, PositiveMovement, NegativeMovement


class CoinWallet(Account):
    student = models.OneToOneField(
        'students.Student', on_delete=models.PROTECT, null=True)


class EngagementWallet(Account):
    student = models.OneToOneField(
        'students.Student', on_delete=models.PROTECT, null=True)
    current_level = models.PositiveSmallIntegerField(null=True, default=1)


class Deposit(PositiveMovement):
    pass


class Withdraw(NegativeMovement):
    pass
