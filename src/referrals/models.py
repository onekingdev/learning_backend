from django.db import models
from app.models import RandomSlugModel, TimestampModel
from users.models import User
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Referral(RandomSlugModel, TimestampModel, MPTTModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,)


    def __str__(self):
        return '{} ({})'.format(self.user or '', self.random_slug)
