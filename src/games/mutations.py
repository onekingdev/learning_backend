import graphene
from graphql import GraphQLError
from wallets.models import CoinWallet
from students.models import Student
from .models import Game, PlayGameTransaction
from students.schema import StudentSchema
from .schema import PlayGameTransactionSchema, GameSchema


class PlayGame(graphene.Mutation):
    """ play game using wallet coins """
    play_game_transaction = graphene.Field(
        PlayGameTransactionSchema)
    student = graphene.Field(StudentSchema)
    game = graphene.Field(GameSchema)

    class Arguments:
        student = graphene.ID(required=True)
        game = graphene.ID(required=True)

    def mutate(self, info, student, game):
        student = Student.objects.get(id=student)
        game = Game.objects.get(id=game)
        account, new = CoinWallet.objects.get_or_create(student=student)
        if account.balance > game.cost:
            play_game_transaction = PlayGameTransaction(
                game=game,
                account=account,
            )
            play_game_transaction.save()
            game.play_stats += 1
            game.save()

            return PlayGame(
                play_game_transaction=play_game_transaction,
                student=student,
                game=game,
            )
        raise GraphQLError('Insufficient balance')


class Mutation(graphene.ObjectType):
    play_game = PlayGame.Field()