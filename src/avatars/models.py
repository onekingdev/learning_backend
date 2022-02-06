from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel
from wallets.models import Withdraw


TYPE_ACCESSORIES = 'ACCESSORIES'
TYPE_HEAD = 'HEAD'
TYPE_CLOTHES = 'CLOTHES'
TYPE_PANTS = 'PANTS'


class Avatar(TimestampModel, UUIDModel, IsActiveModel):
    TYPE_CHOICES = (
        (TYPE_ACCESSORIES, 'Accessories'),
        (TYPE_HEAD, 'Head/Hair'),
        (TYPE_CLOTHES, 'Clothes'),
        (TYPE_PANTS, 'Pants'),
    )

    PREFIX = 'avatar_'

    type_of = models.CharField(max_length=25, null=True, choices=TYPE_CHOICES)
    name = models.CharField(max_length=64, null=True, blank=True)
    image = models.URLField(null=True)
    price = models.DecimalField(
        blank=True, null=True, decimal_places=2, max_digits=15)


class StudentAvatar(TimestampModel, RandomSlugModel, IsActiveModel):
    avatar = models.ForeignKey(
        'avatars.Avatar', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, null=True)
    in_use = models.BooleanField(default=False)


class AvatarPurchaseTransaction(Withdraw):
    avatar = models.ForeignKey(
        Avatar, on_delete=models.PROTECT, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = self.avatar.price
        super().save(*args, **kwargs)
        student_avatar, new = StudentAvatar.objects.get_or_create(
            avatar=self.avatar, student=self.account.student)
        return super().save(*args, **kwargs)