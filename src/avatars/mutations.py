from importlib.metadata import requires
import graphene
from .schema import AvatarSchema, AvatarPurchaseTransactionSchema, StudentAvatarSchema
from .models import Avatar, StudentAvatar, AvatarPurchaseTransaction
from students.models import Student
from students.schema import StudentSchema
from wallets.models import CoinWallet
from graphql import GraphQLError



class PurchaseAvatar(graphene.Mutation):
    """ Purchase a single avatar """
    avatar_purchase_transaction = graphene.Field(
        AvatarPurchaseTransactionSchema)
    student = graphene.Field(StudentSchema)
    avatar = graphene.Field(AvatarSchema)

    class Arguments:
        student = graphene.ID(required=True)
        avatar = graphene.ID(required=True)

    def mutate(self, info, student, avatar):
        student = Student.objects.get(id=student)
        avatar = Avatar.objects.get(id=avatar)
        student_avatar = StudentAvatar.objects.filter(student=student, avatar=avatar)
        if not student_avatar:
            account, new = CoinWallet.objects.get_or_create(student=student)
            avatar_purchase_transaction = AvatarPurchaseTransaction(
                avatar=avatar,
                account=account,
            )
            avatar_purchase_transaction.save()

            return PurchaseAvatar(
                avatar_purchase_transaction=avatar_purchase_transaction,
                student=student,
                avatar=avatar,
            )
        raise GraphQLError('Avatar already purchased')



class CurrentAvatar(graphene.Mutation):
    """ set student_avatars current avatar """
    student_avatar = graphene.Field(StudentAvatarSchema)

    class Arguments:
        student_id = graphene.ID(required=True)
        avatar_id = graphene.ID(required=True)


    def mutate(self, info, student_id, avatar_id):
        student_avatar = StudentAvatar.objects.get(student=student_id, avatar=avatar_id)
        avatar_type = student_avatar.avatar.type_of
        StudentAvatar.objects.filter(student=student_id, avatar__type_of=avatar_type, in_use=True).update(in_use=False)
        student_avatar.in_use = True
        student_avatar.save()

        return CurrentAvatar(
            student_avatar=student_avatar
        )


class Mutation(graphene.ObjectType):
    purchase_avatar = PurchaseAvatar.Field()
    current_avatar = CurrentAvatar.Field()

