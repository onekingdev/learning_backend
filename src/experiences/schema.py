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
    next_level = graphene.Field(LevelSchema, amount=graphene.Int())

    def resolve_levels(root, info, **kwargs):
        # Querying a list
        return Level.objects.all()

    def resolve_level_by_id(root, info, id):
        # Querying a single level
        return Level.objects.get(pk=id)

    def resolve_next_level(root, info, amount) :
        # Querying a single level
        # Get next level from db

        next_levels = Level.objects.filter(amount=amount + 1);
        # If next level not exits, return Null
        if(len(next_levels) > 0):
            return next_levels[0]
        else :
            return  None