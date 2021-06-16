from django.utils.text import slugify
from django.db import models, connection
from accounting.models import Account, Movement, PositiveMovement, NegativeMovement

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

# Create your models here.
class CoinWallet(Account):
    student = models.OneToOneField('students.Student', on_delete=models.PROTECT)


class EngagementWallet(Account):
    student = models.OneToOneField('students.Student', on_delete=models.PROTECT)
    current_level = models.PositiveSmallIntegerField(null=True, default=1)


class Deposit(PositiveMovement):
    pass


class Withdraw(NegativeMovement):
    pass

