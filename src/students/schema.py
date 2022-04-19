import graphene
from django.db.models import Sum
from django.db.models.functions import TruncDay
from datetime import datetime, timedelta
from graphene_django import DjangoObjectType
from students.models import Student, StudentTopicMastery, StudentGrade, StudentAchievement
from audiences.schema import AudienceSchema
from wallets.schema import CoinWalletSchema
from experiences.schema import LevelSchema
from guardians.models import GuardianStudent
from avatars.models import StudentAvatar
from block.models import BlockTransaction


class CoinGraphType(graphene.ObjectType):
    day = graphene.Date()
    coins = graphene.Decimal()

    def resolve_day(self, info):
        return self['day']

    def resolve_coins(self, info):
        return self['coins']


class StudentSchema(DjangoObjectType):
    class Meta:
        model = Student
        fields = "__all__"

    coin_wallet = graphene.Field(CoinWalletSchema)
    grade = graphene.Field('students.schema.StudentGradeSchema')
    next_level = graphene.Field(LevelSchema)
    current_avatar_head = graphene.Field('avatars.schema.AvatarSchema')
    current_avatar_accessories = graphene.Field('avatars.schema.AvatarSchema')
    current_avatar_clothes = graphene.Field('avatars.schema.AvatarSchema')
    current_avatar_pants = graphene.Field('avatars.schema.AvatarSchema')
    user = graphene.Field('users.schema.UserSchema')
    last_week_coins = graphene.List(CoinGraphType)

    def resolve_coin_wallet(self, info):
        return self.coinWallet

    def resolve_grade(self, info):
        student_grade = StudentGrade.objects.filter(
            student_id=self.id, is_active=True).order_by("-create_timestamp")
        if student_grade.count() != 0:
            return student_grade[0]
        return

    def resolve_next_level(self, info):
        # Get next level
        next_level = self.level.get_next_level()
        return next_level

    def resolve_current_avatar_head(self, info):
        try:
            avatar = StudentAvatar.objects.get(
                student=self,
                avatar__type_of='HEAD',
                in_use=True,
            ).avatar
        except StudentAvatar.DoesNotExist:
            avatar = None
        return avatar

    def resolve_current_avatar_accessories(self, info):
        try:
            avatar = StudentAvatar.objects.get(
                student=self,
                avatar__type_of='ACCESSORIES',
                in_use=True,
            ).avatar
        except StudentAvatar.DoesNotExist:
            avatar = None
        return avatar

    def resolve_current_avatar_clothes(self, info):
        try:
            avatar = StudentAvatar.objects.get(
                student=self,
                avatar__type_of='CLOTHES',
                in_use=True,
            ).avatar
        except StudentAvatar.DoesNotExist:
            avatar = None
        return avatar

    def resolve_current_avatar_pants(self, info):
        try:
            avatar = StudentAvatar.objects.get(
                student=self,
                avatar__type_of='PANTS',
                in_use=True,
            ).avatar
        except StudentAvatar.DoesNotExist:
            avatar = None
        return avatar

    def resolve_user(self, info):
        return self.user

    def resolve_last_week_coins(self, info):
        last_week = datetime.now() - timedelta(days=7)
        account = self.coinWallet

        data = (BlockTransaction.objects.filter(account=account)
                .filter(date__gt=last_week)
                .annotate(day=TruncDay("date"))
                .values("day")
                .annotate(coins=Sum("amount"))
                .values("day", "coins")
                .order_by("date")
                )
        
        return data


class StudentTopicMasterySchema(DjangoObjectType):
    class Meta:
        model = StudentTopicMastery
        fields = "__all__"


class StudentGradeSchema(DjangoObjectType):
    class Meta:
        model = StudentGrade
        fields = "__all__"


class StudentAchievementSchema(DjangoObjectType):
    class Meta:
        model = StudentAchievement
        fields = "__all__"


class Query(graphene.ObjectType):

    # ----------------- Student ----------------- #

    students = graphene.List(StudentSchema)
    student_by_id = graphene.Field(StudentSchema, id=graphene.ID())
    students_by_guardian_id = graphene.List(
        StudentSchema, guardian_id=graphene.ID())

    def resolve_students(root, info, **kwargs):
        # Querying a list
        return Student.objects.all()

    def resolve_student_by_id(root, info, id):
        # Querying a single question
        return Student.objects.get(pk=id)

    def resolve_students_by_guardian_id(root, info, guardian_id):
        # Querying a list
        student_list = [
            obj.student for obj in GuardianStudent.objects.filter(
                guardian_id=guardian_id)]
        return student_list

    # ----------------- StudentTopicMastery ----------------- #

    students_topic_mastery = graphene.List(StudentTopicMasterySchema)
    student_topic_mastery_by_id = graphene.Field(
        StudentTopicMasterySchema, id=graphene.ID())

    def resolve_students_topic_mastery(root, info, **kwargs):
        # Querying a list
        return StudentTopicMastery.objects.all()

    def resolve_student_topic_mastery_by_id(root, info, id):
        # Querying a single question
        return StudentTopicMastery.objects.get(pk=id)

    # ----------------- StudentGrade ----------------- #

    students_grade = graphene.List(StudentGradeSchema)
    student_grade_by_id = graphene.Field(
        StudentGradeSchema, id=graphene.ID())

    def resolve_students_grade(root, info, **kwargs):
        # Querying a list
        return StudentGrade.objects.all()

    def resolve_student_grade_by_id(root, info, id):
        # Querying a single question
        return StudentGrade.objects.get(pk=id)

    # ----------------- StudentAchievement ----------------- #

    students_achievement = graphene.List(StudentAchievementSchema)
    student_achievement_by_id = graphene.Field(
        StudentAchievementSchema, id=graphene.ID())

    def resolve_students_achievement(root, info, **kwargs):
        # Querying a list
        return StudentAchievement.objects.all()

    def resolve_student_achievement_by_id(root, info, id):
        # Querying a single question
        return StudentAchievement.objects.get(pk=id)
