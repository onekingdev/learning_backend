from django.db import models
from app.models import TimestampModel, UUIDModel, IsActiveModel
from experiences.models import Level
import datetime

TYPE_ACCESSORIES = 'ACCESSORIES'
TYPE_HEAD = 'HEAD'
TYPE_CLOTHES = 'CLOTHES'
TYPE_PANTS = 'PANTS'


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

    user = models.OneToOneField(
        'users.User',
        on_delete=models.PROTECT,
        null=True
    )
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    full_name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        editable=False)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    points = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    guardian = models.ForeignKey('guardians.Guardian', blank=True, null=True, on_delete=models.PROTECT)
    int_period_start_at = models.DateField(auto_now_add=True)
    student_plan = models.ManyToManyField('plans.StudentPlan')
    active_student_plan = models.ForeignKey(
        'plans.StudentPlan',
        related_name="active_student_plan",
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    avatar_accessories = models.ForeignKey(
        'avatars.Avatar',
        on_delete=models.PROTECT,
        limit_choices_to={'type_of': TYPE_ACCESSORIES},
        related_name='+',
        blank=True,
        null=True
    )
    avatar_head = models.ForeignKey(
        'avatars.Avatar',
        on_delete=models.PROTECT,
        limit_choices_to={'type_of': TYPE_HEAD},
        related_name='+',
        blank=True,
        null=True
    )
    avatar_clothes = models.ForeignKey(
        'avatars.Avatar',
        on_delete=models.PROTECT,
        limit_choices_to={'type_of': TYPE_CLOTHES},
        related_name='+',
        blank=True,
        null=True
    )
    avatar_pants = models.ForeignKey(
        'avatars.Avatar',
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

    @property
    def get_active_audience(self):
        return self.active_group.grade.audience

    @property
    def get_level_number(self):
        return int(self.level.name.split("_")[1]) if(self.level.name) else 0

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name

        if self.pk is None:
            from wallets.models import CoinWallet
            super().save(*args, **kwargs)
            coin_wallet, cw_new = CoinWallet.objects.get_or_create(
                student=self,
                name=self.user.username
            )
            coin_wallet.save()

            from bank.models import BankWallet
            bank_account, ba_new = BankWallet.objects.get_or_create(
                student=self,
                name=self.user.username
            )
            bank_account.save()

            if self.level == None :
                current_level = Level.objects.get(amount = 1)
                self.level = current_level

        return super().save(*args, **kwargs)


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


class StudentTopicGradeStatus(TimestampModel):

    class Status(models.TextChoices):
        BLOCKED = 'B', 'Blocked'
        PREVIEW = 'P', 'Preview'
        AVAILABLE = 'A', 'Available'

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic_grade = models.ForeignKey('kb.TopicGrade', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.BLOCKED,
    )
