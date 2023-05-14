from django.db import models
from django.utils.text import slugify
from app.models import RandomSlugModel, TimestampModel, IsActiveModel


class Group(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'group_'

    name = models.CharField(max_length=128, null=True)
    internal_code = models.CharField(max_length=128, null=True)
    population = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(editable=False)

    grade = models.ForeignKey(
        'kb.Grade', on_delete=models.PROTECT, null=True, blank=True)
    area_of_knowledges = models.ManyToManyField(
        'kb.AreaOfKnowledge', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class School(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'school_'

    name = models.CharField(max_length=128, null=True)
    slug = models.SlugField(editable=False)
    internal_code = models.CharField(max_length=128, null=True)
    type_of = models.CharField(max_length=100, null=True)

    student_plan = models.ManyToManyField('plans.StudentPlan', blank=True)
    organization = models.ForeignKey(
        'organization.Organization', on_delete=models.PROTECT, blank=True)
    # teacher =  models.ManyToManyField('organization.Teacher', blank=True , related_name='teachers')
    student = models.ManyToManyField('students.Student', blank=True)
    group = models.ManyToManyField('organization.Group', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class SchoolPersonnel(TimestampModel, RandomSlugModel, IsActiveModel):
    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDER_OTHER = 'OTHER'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    )

    PREFIX = 'school_personnel_'

    user = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
    school = models.ForeignKey(
        'organization.School', on_delete=models.PROTECT, null=True)

    name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True)
    identification_number = models.CharField(max_length=128, null=True)
    position = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name+' '+self.last_name


class AdministrativePersonnel(SchoolPersonnel):
    pass


class Teacher(SchoolPersonnel):
    pass
