from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


active_roles = (
    ("user", "user"),
    ("manager", "manager")
)


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=120, choices=active_roles, default="user")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
