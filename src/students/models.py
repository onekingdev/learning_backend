from django.db import models
from app.models import TimestampModel, UUIDModel, IsActiveModel
import datetime

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


class Student(TimestampModel, UUIDModel, IsActiveModel):
    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDER_OTHER = 'OTHER'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )

    PREFIX = 'student_'

    user = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    full_name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        editable=False)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)

    student_plan = models.ManyToManyField('plans.StudentPlan')
    active_student_plan = models.ForeignKey(
        'plans.StudentPlan',
        related_name="active_student_plan",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    avatar_accessories = models.ForeignKey(
        Avatar,
        on_delete=models.PROTECT,
        limit_choices_to={'type_of': TYPE_ACCESSORIES},
        related_name='+',
        blank=True,
        null=True
    )
    avatar_head = models.ForeignKey(
        Avatar,
        on_delete=models.PROTECT,
        limit_choices_to={'type_of': TYPE_HEAD},
        related_name='+',
        blank=True,
        null=True
    )
    avatar_clothes = models.ForeignKey(
        Avatar,
        on_delete=models.PROTECT,
        limit_choices_to={'type_of': TYPE_CLOTHES},
        related_name='+',
        blank=True,
        null=True
    )
    avatar_pants = models.ForeignKey(
        Avatar,
        on_delete=models.PROTECT,
        limit_choices_to={'type_of': TYPE_PANTS},
        related_name='+',
        blank=True,
        null=True
    )

    group = models.ManyToManyField('organization.Group', blank=True)
    active_group = models.ForeignKey(
        'organization.Group',
        related_name="active_group",
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    level = models.ForeignKey(
        'experiences.Level',
        on_delete=models.PROTECT,
        null=True)

    def current_age(self):
        today = datetime.date.today()
        birthDate = self.dob

        if self.dob is not None:
            age = (today.year - birthDate.year -
                   ((today.month, today.day) < (birthDate.month, birthDate.day)))
        else:
            age = None
            return age

    @property
    def get_full_name(self):
        return (self.first_name if self.first_name else ' ') + \
            ' ' + (self.last_name if self.last_name else ' ')

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name
        super().save(*args, **kwargs)

        if self.pk is None:
            from wallets.models import CoinWallet, EngagementWallet
            coin_wallet, cw_new = CoinWallet.objects.get_or_create(
                student=self)
            engagement_wallet, ew_new = EngagementWallet.objects.get_or_create(
                student=self)

        return True


class StudentTopicMastery(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'student_topic_mastery_'

    MASTERY_LEVEL_NOT_PRACTICED = 0
    MASTERY_LEVEL_NOVICE = 1
    MASTERY_LEVEL_COMPETENT = 2
    MASTERY_LEVEL_MASTER = 3

    MASTERY_LEVEL_CHOICES = (
        (MASTERY_LEVEL_NOT_PRACTICED, 'Not practiced'),
        (MASTERY_LEVEL_NOVICE, 'Novice'),
        (MASTERY_LEVEL_COMPETENT, 'Competent'),
        (MASTERY_LEVEL_MASTER, 'Master')
    )

    # FK's
    topic_grade = models.ForeignKey(
        'kb.TopicGrade',
        on_delete=models.PROTECT,
        null=True)
    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, null=True)

    # Attributes
    mastery_level = models.CharField(
        max_length=32,
        choices=MASTERY_LEVEL_CHOICES,
        default=0
    )


class StudentGrade(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'student_grade_'
    grade = models.ForeignKey('kb.Grade', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, null=True)
    is_finished = models.IntegerField(null=True)
    percentage = models.FloatField(null=True)
    complete_date = models.DateField(null=True, blank=True)


class StudentAchievement(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'student_achievement_'
    achivement = models.ForeignKey(
        'achievements.Achievement', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, null=True)
    is_liberate = models.IntegerField(null=True)
    liberation_date = models.DateField(null=True, blank=True)
