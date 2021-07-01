import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from experiences.models import Level


class LevelSchema(DjangoObjectType):
    class Meta:
        model = Level
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class Query(graphene.ObjectType):
    levels = graphene.List(LevelSchema)
    level_by_id = graphene.Field(LevelSchema, id=graphene.String())

    def resolve_levels(root, info, **kwargs):
        # Querying a list
        return Level.objects.all()

    def resolve_level_by_id(root, info, id):
        # Querying a single question
        return Level.objects.get(pk=id)
