import graphene
from graphene_django import DjangoObjectType
from bank.models import (
    BankDepositTransaction,
    BankWithdrawTransaction, 
    BankWallet
)
from accounting.models import BankMovement


class BankDepositTransactionSchema(DjangoObjectType):
    class Meta:
        model = BankDepositTransaction
        fields = "__all__"


class BankWithdrawTransactionSchema(DjangoObjectType):
    class Meta:
        model = BankWithdrawTransaction
        fields = "__all__"


class BankWalletSchema(DjangoObjectType):
    class Meta:
        model = BankWallet
        fields = ("balance",)


class BankTransactionSchema(DjangoObjectType):
    class Meta:
        model = BankMovement
        fields = ("amount","date")

    transaction_type = graphene.String()

    def resolve_transaction_type(self,info):
        if self.side == 'L':
            return "withdraw"
        elif self.side == 'R':
            return "deposit"
        return ""


class Query(graphene.ObjectType):
    # ----------------- Student Bank Balance ----------------- #

    student_bank_balance_by_id = graphene.Field(
        BankWalletSchema, student=graphene.ID())

    def resolve_student_bank_balance_by_id(root, info, student):
        # Querying a student's bank balance
        return BankWallet.objects.get(student=student)

    # ----------------- Student Bank Transactions ----------------- #

    student_bank_transactions_by_id = graphene.List(
        BankTransactionSchema, student=graphene.ID())

    def resolve_student_bank_transactions_by_id(root, info, student):
        # Querying a student's transaction
        return BankMovement.objects.filter(account__student=student)

