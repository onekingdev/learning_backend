import graphene
import random
from django.utils import timezone
from students.schema import StudentSchema
from .models import BlockPresentation, Block, BlockTransaction, BlockQuestionPresentation
from .schema import BlockPresentationSchema
from students.models import StudentTopicMastery, StudentTopicStatus
from kb.models import Topic, TopicGrade, AreaOfKnowledge
from kb.models.content import Question, AnswerOption
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
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        student = user.student

        try:
            selected_topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            raise Exception("Topic does not exist")

        # Create block if it doesn't exist
        block = Block.objects.get_or_create(
            students=student,
            topic_grade__topic=selected_topic,
            modality='AI',
        )
        block.save()

        # Create block presentation for block
        block_presentation = BlockPresentation.objects.get_or_create(
            block=block,
            student=student,
        )
        block_presentation.save()

        return CreatePathBlockPresentation(
            block_presentation=block_presentation)


class CreateAIBlockPresentation(graphene.Mutation):
    block_presentation = graphene.Field(BlockPresentationSchema)

    class Arguments:
        student_id = graphene.ID()
        aok_id = graphene.ID(required=True)

    def mutate(self, info, aok_id, student_id=None):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        student = user.student

        # Define weights for status and mastery
        mastery_weights = {'NP': 50, 'N': 30, 'C': 20, 'M': 0}
        status_weights = {'B': 0, 'P': 20, 'A': 80}

        # Find a topic given the AoK
        try:
            area_of_knowledge = AreaOfKnowledge.objects.get(id=aok_id)
        except AreaOfKnowledge.DoesNotExist:
            raise Exception("Area of knowledge does not exist")

        topics = area_of_knowledge.topic_set.all()

        qs1 = StudentTopicStatus.objects.filter(
            student=student,
            topic__in=topics,
        )

        available_status = [
            status['status'] for status in qs1.values('status').distinct()
        ]

        available_status_weights = [
            status_weights[status] for status in available_status
        ]

        status_selection = random.choices(
            population=available_status,
            weights=available_status_weights,
        )[0]

        qs1 = qs1.filter(status=status_selection).values('topic')

        qs2 = StudentTopicMastery.objects.filter(
            student=student,
            topic__in=[topic['topic'] for topic in qs1],
        )

        available_mastery = [
            mastery['mastery_level'] for mastery in qs2.values('mastery_level').distinct()
        ]

        available_mastery_weights = [
            mastery_weights[mastery] for mastery in available_mastery
        ]

        mastery_selection = random.choices(
            population=available_mastery,
            weights=available_mastery_weights,
        )[0]

        qs2 = qs2.filter(mastery_level=mastery_selection).values('topic')

        topic_choice = random.choice(qs2)
        selected_topic = Topic.objects.get(id=topic_choice['topic'])
        topic_grade = TopicGrade.objects.get(topic=selected_topic)

        # Create block if it doesn't exist
        block, new = Block.objects.get_or_create(
            topic_grade=topic_grade,
            modality='AI',
        )
        block.save()
        block.students.add(student)
        block.save()
        if block.questions.all().count() == 0:
            available_questions = list(
                Question.objects.filter(
                    topic=topic_grade.topic).filter(
                    grade=topic_grade.grade))
            if len(available_questions) < block.block_size:
                for question in available_questions:
                    block.questions.add(question)
            else:
                random_questions = random.sample(
                    available_questions, block.block_size)
                for question in random_questions:
                    block.questions.add(question)
        block.save()

        # Create block presentation for block
        block_presentation, new = BlockPresentation.objects.get_or_create(
            block=block,
            student=student,
        )
        block_presentation.save()

        return CreateAIBlockPresentation(block_presentation=block_presentation)


class FinishBlockPresentation(graphene.Mutation):
    block_presentation = graphene.Field(BlockPresentationSchema)
    student = graphene.Field(StudentSchema)

    class Arguments:
        block_presentation_id = graphene.ID(required=True)
        hits = graphene.Int(required=True)
        errors = graphene.Int(required=True)
        bonusCoins = graphene.Float(required=True)
        questions = graphene.List(BlockQuestionInput)

    def mutate(
            self,
            info,
            block_presentation_id,
            hits,
            errors,
            bonusCoins,
            questions):
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
            status = 'CORRECT' if question['is_correct'] else 'INCORRECT'
            question_object = Question.objects.get(id=question['question'])
            answer_object = AnswerOption.objects.get(
                id=question['answer_option'])
            block_question_presentation = BlockQuestionPresentation(
                block_presentation=block_presentation,
                chosen_answer=answer_object,
                question=question_object,
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
            area_of_knowledge=block_aok,
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

        student.update_student_topic_mastery(block_aok)
        student.update_student_topic_status(block_aok)

        block_presentation.delete()

        return FinishBlockPresentation(
            block_presentation=block_presentation,
            student=student)


class Mutation(graphene.ObjectType):
    create_path_block_presentation = CreatePathBlockPresentation.Field()
    create_ai_block_presentation = CreateAIBlockPresentation.Field()
    finish_block_presentation = FinishBlockPresentation.Field()
