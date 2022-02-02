import graphene
from .schema import CollectiblePurchaseTransactionSchema, CollectibleSchema
from .models import Collectible, CollectiblePurchaseTransaction
from students.models import Student
from wallets.models import CoinWallet


class PurchaseCollectiblePack(graphene.Mutation):
    pass


class PurchaseCollectible(graphene.Mutation):
    collectible_purchase_transaction = graphene.Field(
        CollectiblePurchaseTransactionSchema)
    student = graphene.Field('students.schema.StudentSchema')
    collectible = graphene.Field(CollectibleSchema)

    class Arguments:
        student = graphene.ID(required=True)
        collectible = graphene.ID(required=True)

    def mutate(self, info, student, collectible):
        student = Student.objects.get(id=student)
        collectible = Collectible.objects.get(id=collectible)
        account, new = CoinWallet.objects.get_or_create(student=student)

        collectible_purchase_transaction = CollectiblePurchaseTransaction(
            collectible=collectible,
            account=account
        )
        collectible_purchase_transaction.save()

        return PurchaseCollectible(
            collectible_purchase_transaction=collectible_purchase_transaction,
            student=student,
            collectible=collectible,
        )


class Mutation(graphene.ObjectType):
    purchase_collectible = PurchaseCollectible.Field()
