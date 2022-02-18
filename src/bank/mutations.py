from accounting.models import Account
import graphene
from wallets.models import CoinWallet
from students.models import Student
from students.schema import StudentSchema
from bank.schema import (
    BankDepositTransactionSchema,
    BankWithdrawTransactionSchema
)
from bank.models import (
    BankWallet,
    BankDepositTransaction,
    BankDeposit,BankWithdraw,
    BankWithdrawTransaction
)
from graphql import GraphQLError


class BankAccountDeposit(graphene.Mutation):
    """ Bank Transaction """
    student = graphene.Field(StudentSchema)
    bank_deposit_transaction = graphene.Field(
        BankDepositTransactionSchema)

    class Arguments:
        student = graphene.ID(required=True)
        amount = graphene.Float(required=True)

    def mutate(self, info, student, amount):
        student = Student.objects.get(id=student)
        coin_wallet, wc_new = CoinWallet.objects.get_or_create(student=student)
        if coin_wallet.balance > amount:
            bank_account, ba_new = BankWallet.objects.get_or_create(student=student)
            bank_deposit = BankDeposit.objects.create(amount=amount, account=bank_account)
            bank_deposit_transaction = BankDepositTransaction(
                bank_deposit=bank_deposit,amount=amount,
                account=coin_wallet
            )
            bank_deposit_transaction.save()

            return BankAccountDeposit(
                bank_deposit_transaction=bank_deposit_transaction,
                student=student
            )
        raise GraphQLError('Insufficient balance')


class BankAccountWithdraw(graphene.Mutation):
    """ Bank Transaction """
    student = graphene.Field(StudentSchema)
    bank_withdraw_transaction = graphene.Field(
        BankWithdrawTransactionSchema)

    class Arguments:
        student = graphene.ID(required=True)
        amount = graphene.Float(required=True)

    def mutate(self, info, student, amount):
        student = Student.objects.get(id=student)
        coin_wallet, wc_new = CoinWallet.objects.get_or_create(student=student)
        bank_account, ba_new = BankWallet.objects.get_or_create(student=student)
        if bank_account.balance > amount:
            bank_withdraw = BankWithdraw.objects.create(amount=amount, account=bank_account)
            bank_withdraw_transaction = BankWithdrawTransaction(
                bank_withdraw=bank_withdraw,amount=amount,
                account=coin_wallet
            )
            bank_withdraw_transaction.save()

            return BankAccountWithdraw(
                bank_withdraw_transaction=bank_withdraw_transaction,
                student=student
            )
        raise GraphQLError('Insufficient bank balance')


class Mutation(graphene.ObjectType):
    BankAccountDeposit = BankAccountDeposit.Field()
    BankAccountWithdraw = BankAccountWithdraw.Field()