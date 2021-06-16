from django.db import models
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

class Avatar(TimestampModel, UUIDModel, IsActiveModel):
    TYPE_COMPLETE = 'Completo'
    TYPE_TOP = 'Head'
    TYPE_MIDDLE = 'Body'
    TYPE_BOTTOM = 'Legs'
    TYPE_CHOICES = (
        (TYPE_COMPLETE, 'C'),
        (TYPE_TOP, 'H'),
        (TYPE_MIDDLE, 'B'),
        (TYPE_BOTTOM, 'L')
    )

    PREFIX = 'avt_'
    
    type_of = models.CharField(max_length=25, null=True, choices=TYPE_CHOICES)
    
    name = models.CharField(max_length=64, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, help_text='The image of the avatar')
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

class Student(TimestampModel, UUIDModel, IsActiveModel):
    GENDER_MALE = 'Male'
    GENDER_FEMALE = 'Female'
    GENDER_OTHER = 'Other'
    GENDER_CHOICES = (
        (GENDER_MALE, 'M'),
        (GENDER_FEMALE, 'F'),
        (GENDER_OTHER, 'O'),
    )

    PREFIX = 'stdnt_'
    
    user  = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    full_name = models.CharField(max_length=128, null=True, blank=True, editable=False)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=8, null=True, choices=GENDER_CHOICES)

    student_plan = models.ManyToManyField('plans.StudentPlan')
    group =  models.ManyToManyField('organization.Group',blank=True)
    level = models.ForeignKey('experiences.Level', on_delete=models.PROTECT, null=True)
    avatar  = models.ForeignKey('students.Avatar', on_delete=models.PROTECT, null=True)

    def current_age(self):
        today = datetime.date.today()
        birthDate = self.dob
        try:
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        except:
            age = None
            return age

    @property
    def get_full_name(self):
        return (self.first_name if self.first_name else ' ') + (self.last_name if self.last_name else ' ')

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name
        if not self.pk:
            from wallets.models import CoinWallet, EngagementWallet
            coin_wallet, cw_new = CoinWallet.objects.get_or_create(student=self)
            engagement_wallet, ew_new = EngagementWalletWallet.objects.get_or_create(student=self)

        return super().save(*args, **kwargs)

# Create your models here.
class StudentTopicMastery(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'stdn_tpc_mast_'
    topic = models.ForeignKey('kb.Topic', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey('students.Student', on_delete=models.PROTECT, null=True)
    is_mastery = models.IntegerField(null=True)
    is_block = models.IntegerField(null=True)
    date_mastery = models.DateField(null=True, blank=True)

class StudentGrade(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'stdn_tpc_mast_'
    grade = models.ForeignKey('kb.Grade', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey('students.Student', on_delete=models.PROTECT, null=True)
    is_finish = models.IntegerField(null=True)
    percentage = models.FloatField(null=True)
    complete_date = models.DateField(null=True, blank=True)

class StudentAchivement(TimestampModel, UUIDModel, IsActiveModel):
    PREFIX = 'stdn_tpc_mast_'
    achivement = models.ForeignKey('achivements.Achivement', on_delete=models.PROTECT, null=True)
    student = models.ForeignKey('students.Student', on_delete=models.PROTECT, null=True)
    is_liberate = models.IntegerField(null=True)
    liberation_date = models.DateField(null=True, blank=True)
