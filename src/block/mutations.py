import graphene
from django.utils import timezone

from students.schema import StudentSchema
from .models import BlockPresentation, Block, BlockTransaction
from .schema import BlockPresentationSchema
from students.models import Student
from kb.models import Topic
from decimal import Decimal
from wallets.models import CoinWallet


class CreatePathBlockPresentation(graphene.Mutation):
    block_presentation = graphene.Field(BlockPresentationSchema)

    class Arguments:
        student_id = graphene.ID(required=True)
        topic_id = graphene.ID(required=True)

    def mutate(self, info, student_id, topic_id):
        student = Student.objects.get(id=student_id)
        topic = Topic.objects.get(id=topic_id)
        block = Block.objects.filter(
            topic_grade__topic=topic).filter(students=student).first()

        block_presentation, new = BlockPresentation.objects.get_or_create(
            student=student, block=block)
        block_presentation.save()

        return CreatePathBlockPresentation(block_presentation=block_presentation)


class FinishBlockPresentation(graphene.Mutation):
    block_presentation = graphene.Field(BlockPresentationSchema)
    student = graphene.Field(StudentSchema)
    class Arguments:
        block_presentation_id = graphene.ID(required=True)
        hits = graphene.Int(required=True)
        errors = graphene.Int(required=True)
        bonusCoins = graphene.Float(required=True)

    def mutate(self, info, block_presentation_id, hits, errors, bonusCoins):

        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        exp_unit = 1
        coin_unit = 10;
        exp = exp_unit * (hits + errors) + user.student.points

        block_presentation = BlockPresentation.objects.get(
            id=block_presentation_id)
        block_presentation.hits = hits
        block_presentation.errors = errors
        block_presentation.total = hits + errors
        block_presentation.end_timestamp = timezone.now()
        block_presentation.points = exp_unit * (hits + errors)
        block_presentation.bonusCoins = bonusCoins
        block_presentation.coins = coin_unit * hits
        # block_presentation.is_active = False
        block_presentation.save()

        
        #--------------------- level up -S--------------------------------------#
        current_level_amount = user.student.level.amount
        while exp > current_level_amount : 
            next_levels = user.student.level.__class__.objects.filter(amount=current_level_amount + 1);
            if(len(next_levels) < 1): break;
            next_level = next_levels[0]
            if next_level :
                user.student.level = next_level;
                user.student.level.save();
                exp -= current_level_amount
                current_level_amount = next_level.amount
        #--------------------- level up -S--------------------------------------#

        # -------------------- set earned points to student -S------------------#
        student = user.student
        student.points = Decimal(exp)
        student.save()
        # -------------------- set earned points to student -E------------------#

        #--------------------- increase coins and bonus coins on wallet -S------#
        account, new = CoinWallet.objects.get_or_create(student=student)
        
        block_transaction = BlockTransaction(
            blockPresentation=block_presentation,
            account=account,
        )
        block_transaction.save()
        #--------------------- increase coins and bonus coins on wallet -S------#    

        return FinishBlockPresentation(block_presentation = block_presentation, student = student)


class Mutation(graphene.ObjectType):
    create_path_block_presentation = CreatePathBlockPresentation.Field()
    finish_block_presentation = FinishBlockPresentation.Field()
