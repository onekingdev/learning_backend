from django.db import models
from django.utils.text import slugify
from app.models import RandomSlugModel, TimestampModel, IsActiveModel
from payments.models import DiscountCode


class Group(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'group_'

    name = models.CharField(max_length=128, null=True)
    teacher = models.ForeignKey(
        'organization.Teacher', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class School(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'school_'
    SCHOOL_PUBLIC = 'PUBLIC'
    SCHOOL_PRIVATE = 'PRIVATE'
    SCHOOL_CHARTER = 'CHARTER'
    SCHOOL_CHOICES = (
        (SCHOOL_PUBLIC, 'Public'),
        (SCHOOL_PRIVATE, 'Private'),
        (SCHOOL_CHARTER, 'Charter'),
    )

    name = models.CharField(max_length=128, null=True)
    # slug = models.SlugField(editable=False)
    # internal_code = models.CharField(max_length=128, null=True)
    type_of = models.CharField(max_length=15, null=True,  choices=SCHOOL_CHOICES)

    # student_plan = models.ManyToManyField('plans.StudentPlan')
    # organization = models.ForeignKey(
    #     'organization.Organization', on_delete=models.PROTECT, null=True)
    zip = models.CharField(max_length=128, null=True)
    country = models.CharField(max_length=128, null=True)
    coupon_code = models.ForeignKey(
        DiscountCode,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    # student = models.ManyToManyField('students.Student', blank=True)
    # group = models.ManyToManyField('organization.Group', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class SchoolPersonnel(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'school_personnel_'
    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDER_OTHER = 'OTHER'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )


    user = models.OneToOneField(
        'users.User',
        on_delete=models.PROTECT,
        null=True
    )
    school = models.ForeignKey(
        'organization.School',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    has_order = models.BooleanField(default=False)

    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    has_order = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name+' '+self.last_name

class AdministrativePersonnel(SchoolPersonnel):
    PREFIX = 'administrative_personnel_'
    pass

class Teacher(SchoolPersonnel):
    PREFIX = 'teacher_personnel_'
    pass

class Subscriber(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'subscriber_'
    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDER_OTHER = 'OTHER'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )

    PREFIX = 'school_personnel_'

    user = models.OneToOneField(
        'users.User',
        on_delete=models.PROTECT,
        null=True
    )

    has_order = models.BooleanField(default=False)

    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    has_order = models.BooleanField(default=False)

class SubscriberSchool(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'subscriber_school_'

    subscriber = models.OneToOneField(
        Subscriber,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

class Classroom(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'classroom_'
    name = models.CharField(max_length=128, null=True)
    grade = models.ForeignKey(
        'kb.Grade', on_delete=models.PROTECT)
    language = models.CharField(max_length=128, null=True)
    audience = models.ForeignKey(
        'audiences.Audience', on_delete=models.PROTECT)
    # school = models.ForeignKey(School, null=True, on_delete=models.PROTECT)
    # teacher = models.ForeignKey(Teacher, null=True, on_delete=models.PROTECT)
    enable_games = models.BooleanField(default=True)
    game_cost = models.IntegerField(blank=True, null=True)
    time_zone = models.CharField(max_length=128, null=True)
    monday_start = models.TimeField(null=True, editable=True)
    monday_end = models.TimeField(null=True, editable=True)
    tuesday_start = models.TimeField(null=True, editable=True)
    tuesday_end = models.TimeField(null=True, editable=True)
    wednesday_start = models.TimeField(null=True, editable=True)
    wednesday_end = models.TimeField(null=True, editable=True)
    thursday_start = models.TimeField(null=True, editable=True)
    thursday_end = models.TimeField(null=True, editable=True)
    friday_start = models.TimeField(null=True, editable=True)
    friday_end = models.TimeField(null=True, editable=True)
    saturday_start = models.TimeField(null=True, editable=True)
    saturday_end = models.TimeField(null=True, editable=True)
    sunday_start = models.TimeField(null=True, editable=True)
    sunday_end = models.TimeField(null=True, editable=True)

class TeacherClassroom(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'teacher_classroom_'
    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
    )
    plan = models.ForeignKey(
        'plans.Plan',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    order_detail = models.ForeignKey(
        'payments.OrderDetail',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    cancel_reason = models.TextField(blank=True)
    is_cancel = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True)
    period = models.CharField(
        max_length=100,
        choices=(("MONTHLY", "Monthly"), ("YEARLY", "Yearly")),
        default="MONTHLY"
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)

class SchoolTeacher(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'school_teacher_'
    school = models.OneToOneField(
        School,
        on_delete=models.CASCADE,
    )
    teacher = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    plan = models.ForeignKey(
        'plans.Plan',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    order_detail = models.ForeignKey(
        'payments.OrderDetail',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    cancel_reason = models.TextField(blank=True)
    is_cancel = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True)
    period = models.CharField(
        max_length=100,
        choices=(("MONTHLY", "Monthly"), ("YEARLY", "Yearly")),
        default="MONTHLY"
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)