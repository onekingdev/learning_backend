import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from collectibles.models import CollectibleCategory, Collectible, CollectiblePurchaseTransaction, StudentCollectible
from students.models import Student
from wallets.models import CoinWallet


class CollectibleCategorySchema(DjangoObjectType):
    class Meta:
        model = CollectibleCategory
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class CollectibleSchema(DjangoObjectType):
    class Meta:
        model = Collectible
        fields = "__all__"

    name = graphene.String()
    description = graphene.String()
    owned = graphene.Boolean()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)

    def resolve_description(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("description", language_code=current_language)

    def resolve_owned(self, info):
        student = Student.objects.get(user=info.context.user)
        student_collectible = StudentCollectible.objects.filter(
            collectible=self, student=student)
        if student_collectible.exists():
            return True
        else:
            return False


class CollectiblePurchaseTransactionSchema(DjangoObjectType):
    class Meta:
        model = CollectiblePurchaseTransaction
        fields = "__all__"


class StudentCollectilbeSchema(DjangoObjectType):
    class Meta:
        model = StudentCollectible
        fields = "__all__"


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


class Query(graphene.ObjectType):
    # ----------------- CollectibleCategory ----------------- #

    collectibles_category = graphene.List(CollectibleCategorySchema)
    collectible_category_by_id = graphene.Field(
        CollectibleCategorySchema, id=graphene.String())

    def resolve_collectibles_category(root, info, **kwargs):
        # Querying a list
        return CollectibleCategory.objects.all()

    def resolve_collectible_category_by_id(root, info, id):
        # Querying a single question
        return CollectibleCategory.objects.get(pk=id)

    # ----------------- Collectible ----------------- #

    collectibles = graphene.List(CollectibleSchema)
    collectible_by_id = graphene.Field(CollectibleSchema, id=graphene.String())

    def resolve_collectibles(root, info, **kwargs):
        # Querying a list
        return Collectible.objects.all()

    def resolve_collectible_by_id(root, info, id):
        # Querying a single question
        return Collectible.objects.get(pk=id)

    # ----------------- StudentTransactionCollectible ----------------- #

    students_transaction_collectible = graphene.List(
        CollectiblePurchaseTransactionSchema)
    student_transaction_collectible_by_id = graphene.Field(
        CollectiblePurchaseTransactionSchema, id=graphene.String())

    def resolve_students_transaction_collectible(root, info, **kwargs):
        # Querying a list
        return CollectiblePurchaseTransaction.objects.all()

    def resolve_student_transaction_collectible_by_id(root, info, id):
        # Querying a single question
        return CollectiblePurchaseTransaction.objects.get(pk=id)

    # ----------------- StudentCollectible ----------------- #

    students_collectible = graphene.List(
        StudentCollectilbeSchema)
    student_collectible_by_id = graphene.Field(
        StudentCollectilbeSchema, id=graphene.String())

    def resolve_students_collectible(root, info, **kwargs):
        # Querying a list
        return StudentCollectible.objects.all()

    def resolve_student_collectible_by_id(root, info, id):
        # Querying a single question
        return StudentCollectible.objects.get(pk=id)
