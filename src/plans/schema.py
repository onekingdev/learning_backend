import graphene
from graphene_django import DjangoObjectType
from plans.models import StudentPlan


class StudentPlanSchema(DjangoObjectType):
    class Meta:
        model = StudentPlan
        fields = "__all__"


# class StudentPlanTopicGradeSchema(DjangoObjectType):
#     class Meta:
#         model = StudentPlanTopicGrade
#         fields = "__all__"


class Query(graphene.ObjectType):
    # ----------------- StudentPlan ----------------- #

    students_plan = graphene.List(StudentPlanSchema)
    student_plan_by_id = graphene.Field(
        StudentPlanSchema, id=graphene.String())

    def resolve_students_plan(root, info, **kwargs):
        # Querying a list
        return StudentPlan.objects.all()

    def resolve_student_plan_by_id(root, info, id):
        # Querying a single question
        return StudentPlan.objects.get(pk=id)

    # # ----------------- StudentPlanTopicGrade ----------------- #

    # students_plan_topic_grade = graphene.List(StudentPlanTopicGradeSchema)
    # student_plan_topic_grade_by_id = graphene.Field(
    #     StudentPlanTopicGradeSchema, id=graphene.String())

    # def resolve_students_plan_topic_grade(root, info, **kwargs):
    #     # Querying a list
    #     return StudentPlanTopicGrade.objects.all()

    # def resolve_student_plan_topic_grade_by_id(root, info, id):
    #     # Querying a single question
    #     return StudentPlanTopicGrade.objects.get(pk=id)
