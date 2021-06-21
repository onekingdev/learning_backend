from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from app.models import RandomSlugModel, TimestampModel, IsActiveModel, ActiveManager
from wallets.models import Withdraw


# Create your models here.
class CollectibleCategoryManager(ActiveManager, TranslatableManager):
    pass


class CollectibleManager(ActiveManager, TranslatableManager):
    pass


class CollectibleCategory(TimestampModel, MPTTModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=128, null=True),
        description=models.TextField(null=True)
    )

    parent = TreeForeignKey('self', on_delete=models.PROTECT,
                            null=True, blank=True, related_name='sub_categories')

    objects = CollectibleCategoryManager()


class Collectible(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=128, null=True),
        description=models.TextField(null=True)
    )
    price = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=15)
    category = models.ForeignKey(
        'collectibles.CollectibleCategory', on_delete=models.PROTECT, null=True, blank=True)
    objects = CollectibleManager()


class CollectiblePurchaseTransaction(Withdraw):
    collectible = models.ForeignKey(
        'collectibles.Collectible', on_delete=models.PROTECT, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = self.collectible.price
        super().save(*args, **kwargs)
        collectible, new = StudentCollectible.objects.get_or_create(
            collectible=self, student=self.account.coinaccount.student)
        return super().save(*args, **kwargs)


class StudentCollectible(TimestampModel, RandomSlugModel, IsActiveModel):
    collectible = models.ForeignKey(
        'collectibles.Collectible', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, null=True)
