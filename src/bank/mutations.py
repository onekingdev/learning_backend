from accounting.models import Account
import graphene
from wallets.models import CoinWallet
from students.models import Student
from students.schema import StudentSchema
from bank.models import (
    BankWallet,
)
from accounting.models import BankMovement
from .schema import BankMovementSchema
from graphql import GraphQLError

SIDE_CHOICE_DEPOSIT = 'R'
SIDE_CHOICE_WITHDRAW = 'L'

class BankAccountDeposit(graphene.Mutation):
    """ Bank Transaction """
    student = graphene.Field(StudentSchema)
    bankMovement = graphene.Field(BankMovementSchema)
    class Arguments:
        amount = graphene.Float(required=True)

    def mutate(self, info, amount):
        # student = Student.objects.get(id=student)
        student = info.context.user.student
        bank_balance = student.bankWallet.balance
        wallet_balance = student.coinWallet.balance
        print(bank_balance, wallet_balance)
        # coin_wallet, wc_new = CoinWallet.objects.get_or_create(student=student,name=student.user.username)
        # if coin_wallet.balance > amount:
        if wallet_balance > amount:
            bank_account, ba_new = BankWallet.objects.get_or_create(student=student,name=student.user.username)
            bank_deposit = BankMovement.objects.create(amount=amount, account=bank_account, side=SIDE_CHOICE_DEPOSIT)
            print(bank_deposit.date, bank_deposit.amount, bank_account)
            return BankAccountDeposit(student=student, bankMovement=bank_deposit)
        raise GraphQLError('Insufficient balance')


class BankAccountWithdraw(graphene.Mutation):
    """ Bank Transaction """
    student = graphene.Field(StudentSchema)
    bankMovement = graphene.Field(
        BankMovementSchema)

    class Arguments:
        amount = graphene.Float(required=True)

    def mutate(self, info, amount):
        # student = Student.objects.get(id=student)
        student = info.context.user.student
        bank_balance = student.bankWallet.balance
        wallet_balance = student.coinWallet.balance
        # coin_wallet, wc_new = CoinWallet.objects.get_or_create(student=student,name=student.user.username)
        # print("123",coin_wallet, coin_wallet.balance)
        # if coin_wallet.balance > amount:
        if bank_balance > amount:
            bank_account, ba_new = BankWallet.objects.get_or_create(student=student,name=student.user.username)
            bank_withdraw = BankMovement.objects.create(amount=amount, account=bank_account, side=SIDE_CHOICE_WITHDRAW)
            return BankAccountWithdraw(
                bankMovement=bank_withdraw,
                student=student
            )
        raise GraphQLError('Insufficient balance')


class Mutation(graphene.ObjectType):
    BankAccountDeposit = BankAccountDeposit.Field()
    BankAccountWithdraw = BankAccountWithdraw.Field()