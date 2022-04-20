import graphene
from graphene_django import DjangoObjectType
from .models import DailyTreasure, DailyTreasureLevel, StudentDailyTreasure


class DailyTreasureSchema(DjangoObjectType):
    class Meta:
        model = DailyTreasure
        fields = "__all__"


class DailyTreasureLevelSchema(DjangoObjectType):
    class Meta:
        model = DailyTreasureLevel
        fields = "__all__"


class StudentDailyTreasureSchema(DjangoObjectType):
    class Meta:
        model = StudentDailyTreasure
        fields = "__all__"


class Query(graphene.ObjectType):

    # ----------------- DailyTreasure ----------------- #

    daily_treasures = graphene.List(DailyTreasureSchema)
    daily_treasure_by_id = graphene.Field(
        DailyTreasureSchema,
        id=graphene.ID()
    )

    def resolve_daily_treasures(root, info, **kwargs):
        return DailyTreasure.objects.all()

    def resolve_daily_treasure_by_id(root, info, id):
        return DailyTreasure.objects.get(id=id)

    # ----------------- DailyTreasureLevel ----------------- #

    daily_treasure_levels = graphene.List(DailyTreasureLevelSchema)
    daily_treasure_level_by_id = graphene.Field(
        DailyTreasureLevelSchema,
        id=graphene.ID()
    )

    def resolve_daily_treasure_levels(root, info, **kwargs):
        return DailyTreasureLevel.objects.all()

    def resolve_daily_treasure_level_by_id(root, info, id):
        return DailyTreasureLevel.objects.get(id=id)

    # ----------------- StudentDailyTreasure ----------------- #

    student_daily_treasures = graphene.List(StudentDailyTreasureSchema)
    student_daily_treasure_by_id = graphene.Field(
        StudentDailyTreasureSchema,
        id=graphene.ID()
    )

    def resolve_student_daily_treasures(root, info, **kwargs):
        return StudentDailyTreasure.objects.all()

    def resolve_student_daily_treasure_by_id(root, info, id):
        return StudentDailyTreasure.objects.get(id=id)
