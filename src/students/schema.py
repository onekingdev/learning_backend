import graphene
from graphene_django import DjangoObjectType
from students.models import Avatar, Student, StudentTopicMastery, StudentGrade, StudentAchievement


class AvatarSchema(DjangoObjectType):
    class Meta:
        model = Avatar
        fields = "__all__"


class StudentSchema(DjangoObjectType):
    class Meta:
        model = Student
        fields = "__all__"


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


class SetStudentAvatar(graphene.Mutation):
    avatar_url = graphene.String()
    student_id = graphene.ID()
    avatar_type_of = graphene.Enum(
        'TypeOf',
        [
            ('Accesories', 1),
            ('Head/Hair', 2),
            ('Clothes', 3),
            ('Pants', 4)]
    )

    class Arguments:
        avatar_url = graphene.String()
        student_id = graphene.ID()
        avatar_type_of = graphene.Enum(
            'TypeOf',
            [
                ('Accesories', 1),
                ('Head/Hair', 2),
                ('Clothes', 3),
                ('Pants', 4)]
        )

    def mutate(self, info, avatar_url, student_id, avatar_type_of):
        student = Student.objects.get(id=student_id)
        avatar = Avatar.objects.get_or_create(
            image=avatar_url,
            type_of=avatar_type_of)

        avatar.save()

        if avatar_type_of == 1:
            student.avatar_accessories = avatar
        elif avatar_type_of == 2:
            student.avatar_head = avatar
        elif avatar_type_of == 3:
            student.avatar_clothes = avatar
        else:
            student.avatar_pants = avatar

        student.save()


class Query(graphene.ObjectType):
    # ----------------- Avatar ----------------- #

    avatars = graphene.List(AvatarSchema)
    avatar_by_id = graphene.Field(AvatarSchema, id=graphene.String())

    def resolve_avatars(root, info, **kwargs):
        # Querying a list
        return Avatar.objects.all()

    def resolve_avatar_by_id(root, info, id):
        # Querying a single question
        return Avatar.objects.get(pk=id)

    # ----------------- Student ----------------- #

    students = graphene.List(StudentSchema)
    student_by_id = graphene.Field(StudentSchema, id=graphene.String())

    def resolve_students(root, info, **kwargs):
        # Querying a list
        return Student.objects.all()

    def resolve_student_by_id(root, info, id):
        # Querying a single question
        return Student.objects.get(pk=id)

    # ----------------- StudentTopicMastery ----------------- #

    students_topic_mastery = graphene.List(StudentTopicMasterySchema)
    student_topic_mastery_by_id = graphene.Field(
        StudentTopicMasterySchema, id=graphene.String())

    def resolve_students_topic_mastery(root, info, **kwargs):
        # Querying a list
        return StudentTopicMastery.objects.all()

    def resolve_student_topic_mastery_by_id(root, info, id):
        # Querying a single question
        return StudentTopicMastery.objects.get(pk=id)

    # ----------------- StudentGrade ----------------- #

    students_grade = graphene.List(StudentGradeSchema)
    student_grade_by_id = graphene.Field(
        StudentGradeSchema, id=graphene.String())

    def resolve_students_grade(root, info, **kwargs):
        # Querying a list
        return StudentGrade.objects.all()

    def resolve_student_grade_by_id(root, info, id):
        # Querying a single question
        return StudentGrade.objects.get(pk=id)

    # ----------------- StudentAchievement ----------------- #

    students_achievement = graphene.List(StudentAchievementSchema)
    student_achievement_by_id = graphene.Field(
        StudentAchievementSchema, id=graphene.String())

    def resolve_students_achievement(root, info, **kwargs):
        # Querying a list
        return StudentAchievement.objects.all()

    def resolve_student_achievement_by_id(root, info, id):
        # Querying a single question
        return StudentAchievement.objects.get(pk=id)
