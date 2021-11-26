from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager, TreeQuerySet
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from parler.managers import TranslatableQuerySet
from app.models import RandomSlugModel, TimestampModel, IsActiveModel, ActiveManager
from wallets.models import Withdraw


class CollectibleCategoryQuerySet(TranslatableQuerySet, TreeQuerySet):
    def as_manager(cls):
        manager = CollectibleCategoryManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager
    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


class CollectibleCategoryManager(ActiveManager, TreeManager, TranslatableManager):
    _queryset_class = CollectibleCategoryQuerySet


class CollectibleManager(ActiveManager, TranslatableManager):
    pass


class CollectibleCategory(TimestampModel, MPTTModel, RandomSlugModel, TranslatableModel, IsActiveModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=128, null=True),
        description=models.TextField(null=True)
    )

    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='sub_categories'
    )

    image = models.ImageField()

    objects = CollectibleCategoryManager()


class Collectible(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=128, null=True),
        description=models.TextField(null=True)
    )
    image = models.ImageField()
    price = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=15)
    category = models.ForeignKey(
        'collectibles.CollectibleCategory', on_delete=models.PROTECT, null=True, blank=True)
    objects = CollectibleManager()

    # TODO: - Collectible tiers (rarity)
    #       - Collectible type (cards, etc)


class CollectiblePurchaseTransaction(Withdraw):
    collectible = models.ForeignKey(
        'collectibles.Collectible', on_delete=models.PROTECT, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = self.collectible.price
        super().save(*args, **kwargs)
        student_collectible, new = StudentCollectible.objects.get_or_create(
            collectible=self.collectible, student=self.account.student)
        return super().save(*args, **kwargs)


class StudentCollectible(TimestampModel, RandomSlugModel, IsActiveModel):
    collectible = models.ForeignKey(
        'collectibles.Collectible', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, null=True)
