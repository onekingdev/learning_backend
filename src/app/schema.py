import graphene
from graphene_django import DjangoObjectType

from students.models import Student

class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = ("first_name", "last_name", "age")


class Query(graphene.Objecttype):
    all_students = graphene.List(StudentType)

    def resolve_all_students(root, info):
        return Student.objects.all()


schema = graphene.Schema(query=Query)
