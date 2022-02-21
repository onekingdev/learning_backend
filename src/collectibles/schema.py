import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from collectibles.models import CollectibleCategory, Collectible, StudentCollectible
from .models import CollectiblePurchaseTransaction, CollectiblePackPurchaseTransaction
from students.models import Student


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

        return self.safe_translation_getter(
            "name", language_code=current_language)


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

        return self.safe_translation_getter(
            "name", language_code=current_language)

    def resolve_description(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter(
            "description", language_code=current_language)

    def resolve_owned(self, info):
        student = Student.objects.get(user=info.context.user)
        student_collectible = StudentCollectible.objects.filter(
            collectible=self, student=student)
        if student_collectible.exists():
            return True
        else:
            return False

    def resolve_amount(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("User is not authenticated")
        if user.student is None:
            raise Exception("User is not a student")
        student = Student.objects.get(user=info.content.user)
        student_collectible = StudentCollectible.objects.filter(
            collectible=self, student=student)
        if student_collectible.exists():
            return student_collectible.amount
        else:
            return 0


class CollectiblePurchaseTransactionSchema(DjangoObjectType):
    class Meta:
        model = CollectiblePurchaseTransaction
        fields = "__all__"


class CollectiblePackPurchaseTransactionSchema(DjangoObjectType):
    class Meta:
        model = CollectiblePackPurchaseTransaction
        fields = "__all__"


class StudentCollectilbeSchema(DjangoObjectType):
    class Meta:
        model = StudentCollectible
        fields = "__all__"


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
    collectibles_not_owned = graphene.Field(CollectibleSchema)

    def resolve_collectibles(root, info, **kwargs):
        # Querying a list
        return Collectible.objects.all()

    def resolve_collectible_by_id(root, info, id):
        # Querying a single question
        return Collectible.objects.get(pk=id)

    def resolve_collectibles_not_owned(root, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("User not authenticated")
        if user.student is None:
            raise Exception("User has no student")

        student = user.student

        owned_collectibles = Collectible.objects.filter(
            studentcollectible__student=student
        )
        all_collectibles = Collectible.objects.all()
        not_owned = all_collectibles.difference(owned_collectibles)

        return not_owned

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
