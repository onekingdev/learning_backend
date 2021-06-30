from django.db import models
from app.models import TimestampModel, UUIDModel, IsActiveModel
import datetime


class Avatar(TimestampModel, UUIDModel, IsActiveModel):
    TYPE_COMPLETE = 'COMPLETE'
    TYPE_TOP = 'HEAD'
    TYPE_MIDDLE = 'BODY'
    TYPE_BOTTOM = 'LEGS'
    TYPE_CHOICES = (
        (TYPE_COMPLETE, 'Complete'),
        (TYPE_TOP, 'Head'),
        (TYPE_MIDDLE, 'Body'),
        (TYPE_BOTTOM, 'Legs')
    )

    PREFIX = 'avatar_'

    type_of = models.CharField(max_length=25, null=True, choices=TYPE_CHOICES)
    name = models.CharField(max_length=64, null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              help_text='The image of the avatar')


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
        max_length=128, null=True, blank=True, editable=False)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)

    student_plan = models.ManyToManyField('plans.StudentPlan')
    group = models.ManyToManyField('organization.Group', blank=True)
    level = models.ForeignKey(
        'experiences.Level', on_delete=models.PROTECT, null=True)
    avatar = models.ForeignKey(
        'students.Avatar', on_delete=models.PROTECT, null=True, blank=True)

    def current_age(self):
        today = datetime.date.today()
        birthDate = self.dob
        try:
            age = today.year - birthDate.year - \
                ((today.month, today.day) < (birthDate.month, birthDate.day))
        except:
            age = None
            return age

    @property
    def get_full_name(self):
        return (self.first_name if self.first_name else ' ') + ' ' + (self.last_name if self.last_name else ' ')

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

# Create your models here.


class StudentTopicMastery(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'student_topic_mastery_'
    topic = models.ForeignKey('kb.Topic', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, null=True)
    is_mastery = models.IntegerField(null=True)
    is_block = models.IntegerField(null=True)
    date_mastery = models.DateField(null=True, blank=True)


class StudentGrade(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'student_grade_'
    grade = models.ForeignKey('kb.Grade', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, null=True)
    is_finish = models.IntegerField(null=True)
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
