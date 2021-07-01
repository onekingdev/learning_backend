import graphene
from graphene_django import DjangoObjectType
from guardians.models import Guardian, GuardianStudent


class GuardianSchema(DjangoObjectType):
    class Meta:
        model = Guardian
        fields = "__all__"


class GuardianStudentSchema(DjangoObjectType):
    class Meta:
        model = GuardianStudent
        fields = "__all__"


class Query(graphene.ObjectType):
    # ----------------- Guardian ----------------- #

    guardians = graphene.List(GuardianSchema)
    guardian_by_id = graphene.Field(GuardianSchema, id=graphene.String())

    def resolve_guardians(root, info, **kwargs):
        # Querying a list
        return Guardian.objects.all()

    def resolve_guardian_by_id(root, info, id):
        # Querying a single question
        return Guardian.objects.get(pk=id)

    # ----------------- GuardianStudent ----------------- #

    guardians_student = graphene.List(GuardianStudentSchema)
    guardian_student_by_id = graphene.Field(
        GuardianStudentSchema, id=graphene.String())
    guardian_student_by_guardian = graphene.List(
        GuardianStudentSchema, id=graphene.ID())

    def resolve_guardians_student(root, info, **kwargs):
        # Querying a list
        return GuardianStudent.objects.all()

    def resolve_guardian_student_by_id(root, info, id):
        # Querying a single question
        return GuardianStudent.objects.get(pk=id)

    def resolve_guardian_student_by_guardian(root, info, id):
        # Querying a single question
        return GuardianStudent.objects.filter(guardian=id)
