from django.db import models
from app.models import TimestampModel, UUIDModel, IsActiveModel
from engine.models import TopicMasterySettings
from block.models import BlockQuestionPresentation
import datetime

TYPE_ACCESSORIES = 'ACCESSORIES'
TYPE_HEAD = 'HEAD'
TYPE_CLOTHES = 'CLOTHES'
TYPE_PANTS = 'PANTS'


class StudentTopicStatus(TimestampModel):
    class Status(models.TextChoices):
        BLOCKED = 'B', 'Blocked'
        PREVIEW = 'P', 'Preview'
        AVAILABLE = 'A', 'Available'

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    topic = models.ForeignKey(
        'kb.Topic',
        on_delete=models.CASCADE,
        related_name='status'
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.BLOCKED,
    )


class StudentTopicMastery(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'student_topic_mastery_'

    MASTERY_LEVEL_NOT_PRACTICED = 'NP'
    MASTERY_LEVEL_NOVICE = 'N'
    MASTERY_LEVEL_COMPETENT = 'C'
    MASTERY_LEVEL_MASTER = 'M'

    MASTERY_LEVEL_CHOICES = (
        (MASTERY_LEVEL_NOT_PRACTICED, 'Not practiced'),
        (MASTERY_LEVEL_NOVICE, 'Novice'),
        (MASTERY_LEVEL_COMPETENT, 'Competent'),
        (MASTERY_LEVEL_MASTER, 'Master')
    )

    # FK's
    topic = models.ForeignKey(
        'kb.Topic',
        on_delete=models.PROTECT,
        related_name='mastery',
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.PROTECT,
    )

    # Attributes
    mastery_level = models.CharField(
        max_length=3,
        choices=MASTERY_LEVEL_CHOICES,
        default='NP'
    )


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
    points = models.IntegerField(default=0)
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
        return int(self.level.name.split("_")[1]) if (self.level.name) else 0

    def init_student_topic_mastery(self):
        from plans.models import GuardianStudentPlan
        from kb.models import AreaOfKnowledge
        try:
            available_aoks = GuardianStudentPlan.objects.get(
                student=self).subject
        except GuardianStudentPlan.DoesNotExist:
            audience = self.get_active_audience
            available_aoks = AreaOfKnowledge.objects.filter(audience=audience)

        for aok in available_aoks:
            topics = aok.topic_set.all()
            for topic in topics:
                topic_mastery = StudentTopicMastery(
                    student=self,
                    topic=topic,
                )
                topic_mastery.save()

    def update_student_topic_mastery(self, aok):
        topics = aok.topic_set.all()

        for topic in topics:
            mastery_settings, new = TopicMasterySettings.objects.get_or_create(
                topic=topic
            )
            total_correct = 0
            sample_size = mastery_settings.sample_size
            mastery_percentage = mastery_settings.mastery_percentage/100
            competence_percentage = mastery_settings.competence_percentage/100
            # Get last N questions from topic sorted by date
            last_questions = BlockQuestionPresentation.all_objects.filter(
                topic=topic
            ).order_by('-create_timestamp')[:sample_size]
            for question in last_questions:
                if question.is_correct:
                    total_correct += 1
            if total_correct == 0:
                mastery_level = 'NP'
            elif total_correct < sample_size*mastery_percentage*competence_percentage:
                mastery_level = 'N'
            elif total_correct < sample_size*mastery_percentage:
                mastery_level = 'C'
            else:
                mastery_level = 'M'
            student_topic_mastery, new = StudentTopicMastery.objects.get_or_create(
                student=self,
                topic=topic,
            )
            student_topic_mastery.mastery_level = mastery_level
            student_topic_mastery.save()

    def init_student_topic_status(self):
        from plans.models import GuardianStudentPlan
        from kb.models import AreaOfKnowledge
        try:
            available_aoks = GuardianStudentPlan.objects.get(
                student=self).subject
        except GuardianStudentPlan.DoesNotExist:
            audience = self.get_active_audience
            available_aoks = AreaOfKnowledge.objects.filter(audience=audience)

        for aok in available_aoks:
            topics = aok.topic_set.all()
            for topic in topics:
                if topic.prerequisites is None:
                    status = 'A'
                else:
                    prerequisites = topic.prerequisites
                    prerequisites_mastery = []
                    for prerequisite in prerequisites:
                        prerequisites_mastery.append(
                            prerequisite.mastery_level.mastery_level
                        )
                    if 'NP' in prerequisites_mastery:
                        status = 'B'
                    elif 'N' in prerequisites_mastery:
                        status = 'B'
                    elif 'C' in prerequisites_mastery:
                        status = 'P'
                    else:
                        status = 'A'
                topic_status = StudentTopicStatus(
                    student=self,
                    topic=topic,
                    status=status,
                )
                topic_status.save()

    def update_student_topic_status(self, aok):
        topics = aok.topic_set.all()

        topics = aok.topic_set.all()
        for topic in topics:
            if topic.prerequisites is None:
                status = 'A'
            else:
                prerequisites = topic.prerequisites
                prerequisites_mastery = []
                for prerequisite in prerequisites:
                    prerequisites_mastery.append(
                        prerequisite.mastery_level.mastery_level
                    )
                if 'NP' in prerequisites_mastery:
                    status = 'B'
                elif 'N' in prerequisites_mastery:
                    status = 'B'
                elif 'C' in prerequisites_mastery:
                    status = 'P'
                else:
                    status = 'A'
            topic_status, new = StudentTopicStatus.objects.get_or_create(
                student=self,
                topic=topic,
            )
            topic_status.status = status
            topic_status.save()

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

            self.init_student_topic_mastery()
            self.init_student_topic_status()

        return super().save(*args, **kwargs)


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
