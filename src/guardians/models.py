from django.db import models
from app.models import RandomSlugModel, TimestampModel, IsActiveModel


class Guardian(TimestampModel, RandomSlugModel, IsActiveModel):
    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDER_OTHER = 'OTHER'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )

    PREFIX = 'guardian_'

    name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    user = models.OneToOneField(
        'users.User',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.user.username


class GuardianStudent(TimestampModel, RandomSlugModel):
    PREFIX = "guardian_student_"

    guardian = models.ForeignKey(
        'guardians.Guardian',
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.PROTECT,
        null=True,
        blank=True)
