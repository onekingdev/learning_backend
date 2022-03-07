import graphene
from django.utils import timezone
from students.schema import StudentSchema
from .models import BlockPresentation, Block, BlockTransaction, BlockQuestionPresentation
from .schema import BlockPresentationSchema
from students.models import Student
from kb.models import Topic
from engine.models import TopicStudentReport, AreaOfKnowledgeStudentReport
from decimal import Decimal
from wallets.models import CoinWallet


class BlockQuestionInput(graphene.InputObjectType):
    question = graphene.ID()
    answer_option = graphene.ID()
    is_correct = graphene.Boolean()


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

        return CreatePathBlockPresentation(
            block_presentation=block_presentation)


class FinishBlockPresentation(graphene.Mutation):
    block_presentation = graphene.Field(BlockPresentationSchema)
    student = graphene.Field(StudentSchema)

    class Arguments:
        block_presentation_id = graphene.ID(required=True)
        hits = graphene.Int(required=True)
        errors = graphene.Int(required=True)
        bonusCoins = graphene.Float(required=True)
        questions = graphene.List(BlockQuestionInput)

    def mutate(self, info, block_presentation_id, hits, errors, bonusCoins, questions):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        student = user.student

        exp_unit = 5
        coin_unit = 10
        exp = exp_unit * (hits + errors) + user.student.points

        # Assign values to BlockPresentation
        block_presentation = BlockPresentation.objects.get(
            id=block_presentation_id
        )
        block_presentation.hits = hits
        block_presentation.errors = errors
        block_presentation.total = hits + errors
        block_presentation.end_timestamp = timezone.now()
        block_presentation.points = exp_unit * (hits + errors)
        block_presentation.bonusCoins = bonusCoins
        block_presentation.coins = coin_unit * hits
        block_presentation.save()

        # Create registers on BlockQuestionPresentation
        block_topic = block_presentation.block.topic_grade.topic
        block_aok = block_topic.area_of_knowledge
        for question in questions:
            status = 'CORRECT' if question.is_correct else 'INCORRECT'
            block_question_presentation = BlockQuestionPresentation(
                block_presentation=block_presentation,
                chowsen_answer=question.answer_option,
                question=question.question,
                status=status,
                topic=block_topic,
            )
            block_question_presentation.save()

        # Create registers for report tables
        topic_report, new = TopicStudentReport.objects.get_or_create(
            topic=block_topic,
            student=student,
        )
        topic_report.questions_answered += block_presentation.total
        topic_report.correct_question += block_presentation.hits
        topic_report.save()

        aok_report, new = AreaOfKnowledgeStudentReport.objects.get_or_create(
            aok=block_aok,
            student=student,
        )
        aok_report.questions_answered += block_presentation.total
        aok_report.correct_question += block_presentation.hits
        aok_report.save()

        while exp > student.level.points_required:
            exp -= student.level.points_required
            next_level = student.level.get_next_level()
            student.level = next_level

        student.points = Decimal(exp)
        student.save()

        account, new = CoinWallet.objects.get_or_create(student=student)

        block_transaction = BlockTransaction(
            blockPresentation=block_presentation,
            account=account,
        )
        block_transaction.save()

        return FinishBlockPresentation(
            block_presentation=block_presentation,
            student=student)


class Mutation(graphene.ObjectType):
    create_path_block_presentation = CreatePathBlockPresentation.Field()
    finish_block_presentation = FinishBlockPresentation.Field()
