import graphene
from django.utils import timezone
from .models import DailyTreasure, StudentDailyTreasure, DailyTreasureTransaction
from student.models import Student


class RedeemDailyTreasure(graphene.Mutation):
    student_daily_treasure = graphene.Field(
        'treasuretrack.schema.StudentDailyTreasureSchema'
    )
    daily_treasure_transaction = graphene.Field(
        'treasuretrack.schema.DailyTreasureTransaction'
    )

    class Arguments:
        student_id = graphene.ID()
        daily_treasure_id = graphene.ID(required=True)

    def mutate(self, info, daily_treasure_id, student_id=None):
        if student_id is None:
            user = info.context.user

            if not user.is_authenticated:
                raise Exception("Authentication credentials were not provided")
            if not user.student:
                raise Exception("Not found student")

            student = user.student
        else:
            student = Student.objects.get(id=student_id)

        daily_treasure = DailyTreasure.objects.get(id=daily_treasure_id)

        student_daily_treasure, new = StudentDailyTreasure.objects.get_or_create(
            student=student,
            daily_treasure=daily_treasure,
            create_timestamp=timezone.now().date()
        )

        if new:
            daily_treasure_transaction = DailyTreasureTransaction(
                daily_treasure=daily_treasure,
                account=student.coinWallet
            )

        return RedeemDailyTreasure(
            student_daily_treasure=student_daily_treasure,
            daily_treasure_transaction=daily_treasure_transaction
        )


class Mutation(graphene.ObjectType):
    redeem_daily_treasure = RedeemDailyTreasure.Field()
