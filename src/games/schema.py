from unicodedata import category
import graphene
from graphene_django import DjangoObjectType
from .models import Game, PlayGameTransaction, GameCategory

class GameSchema(DjangoObjectType):
    class Meta:
        model = Game
        fields = "__all__"


class PlayGameTransactionSchema(DjangoObjectType):
    class Meta:
        model = PlayGameTransaction
        fields = "__all__"


class GameCategorySchema(DjangoObjectType):
    class Meta:
        model = GameCategory
        fields = "__all__"


class Query(graphene.ObjectType):
    # ----------------- GameCategory ----------------- #

    games_category = graphene.List(GameCategorySchema)
    game_category_by_id = graphene.Field(
        GameCategorySchema, id=graphene.ID())

    def resolve_games_category(root, info, **kwargs):
        # Querying a list
        return GameCategory.objects.all()

    def resolve_game_category_by_id(root, info, id):
        # Querying a single game category
        return GameCategory.objects.get(pk=id)
    

    # ----------------- Game ----------------- #

    games = graphene.List(GameSchema)
    game_by_id = graphene.Field(GameSchema, id=graphene.ID())

    def resolve_games(root, info, **kwargs):
        # Querying a list
        return Game.objects.all()

    def resolve_game_by_id(root, info, id):
        # Querying a single game
        return Game.objects.get(pk=id)

    # ----------------- Games by Category ID ----------------- #

    games_by_category_id = graphene.List(GameSchema, category=graphene.ID())

    def resolve_games_by_category_id(root, info, category):
        # Querying a game list by category
        return Game.objects.filter(category=category)
