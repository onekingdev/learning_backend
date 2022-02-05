import graphene
from graphene_django import DjangoObjectType
from .models import CoinWallet


class CoinWalletSchema(DjangoObjectType):
    class Meta:
        model = CoinWallet
        fields = "__all__"


class Query(graphene.ObjectType):
    # ----------------- CoinWallet ----------------- #

    coin_wallet = graphene.List(CoinWalletSchema)
    coin_wallet_by_id = graphene.Field(CoinWalletSchema, id=graphene.ID())

    def resolve_coin_wallet(root, info, **kwargs):
        # Querying a list
        return CoinWallet.objects.all()

    def resolve_coin_wallet_by_id(root, info, id):
        # Querying a single question
        return CoinWallet.objects.get(pk=id)
