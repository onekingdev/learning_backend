import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from api.models import profile
from django.contrib.auth.models import User


class UserSchema(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserProfileSchema(DjangoObjectType):
    class Meta:
        model = profile


class Query(graphene.ObjectType):

    # ----------------- User ----------------- #

    users = graphene.List(UserSchema)
    user_by_id = graphene.Field(UserSchema, id=graphene.ID())

    def resolve_users(root, info, **kwargs):
        # Querying a list
        return User.objects.all()

    def resolve_user_by_id(root, info, id):
        # Querying a single question
        return User.objects.get(pk=id)
