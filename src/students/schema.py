import graphene
from graphene_django import DjangoObjectType
from students.models import Student, StudentTopicMastery, StudentGrade, StudentAchievement
from audiences.schema import AudienceSchema
from wallets.schema import CoinWalletSchema
from experiences.schema import LevelSchema

class StudentSchema(DjangoObjectType):
    class Meta:
        model = Student
        fields = "__all__"

    audience = graphene.Field(AudienceSchema)
    coin_wallet = graphene.Field(CoinWalletSchema)
    grade = graphene.Field('students.schema.StudentGradeSchema')
    next_level = graphene.Field(LevelSchema)

    def resolve_audience(self, info):
        return self.get_active_audience

    def resolve_coin_wallet(self, info):
        return self.coinWallet

    def resolve_grade(self, info):
        student_grade = StudentGrade.objects.filter(student_id=self.id, is_active=True)
        if student_grade.count() != 0:
            return student_grade[0]
        return
    
    def resolve_next_level(self, info):
        # Querying a single next level
        current_level = self.level;
        # Get next level
        next_level = self.level.get_next_level()
        return next_level


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

    def resolve_students(root, info, **kwargs):
        # Querying a list
        return Student.objects.all()

    def resolve_student_by_id(root, info, id):
        # Querying a single question
        return Student.objects.get(pk=id)

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
