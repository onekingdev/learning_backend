from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from api.models import profile


class UserSchema(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserProfileSchema(DjangoObjectType):
    class Meta:
        model = profile
