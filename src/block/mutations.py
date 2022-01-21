import graphene
from django.utils import timezone
from .models import BlockPresentation, Block
from students.models import Student
from .schema import BlockPresentationSchema


class CreatePathBlockPresentation(graphene.Mutation):
    block_presentation = graphene.Field(BlockPresentationSchema)

    class Arguments:
        block_id = graphene.ID(required=True)
        student_id = graphene.ID(required=True)

    def mutate(self, info, student_id, block_id):
        student = Student.objects.get(id=student_id)
        block = Block.objects.get(id=block_id)

        block_presentation, new = BlockPresentation.objects.get_or_create(
            student=student, block=block)
        block_presentation.start_timestamp = timezone.now()
        block_presentation.save()

        return CreatePathBlockPresentation(block_presentation=block_presentation)


class FinishBlockPresentation(graphene.Mutation):
    block_presentation = graphene.Field(BlockPresentationSchema)

    class Arguments:
        block_presentation_id = graphene.ID(required=True)
        hits = graphene.Int(required=True)
        errors = graphene.Int(required=True)

    def mutate(self, info, block_presentation_id, hits, errors):
        block_presentation = BlockPresentation.objects.get(
            id=block_presentation_id)
        block_presentation.hits = hits
        block_presentation.errors = errors
        block_presentation.total = hits + errors
        block_presentation.end_timestamp = timezone.now()
        block_presentation.is_active = False
        block_presentation.save()

        return FinishBlockPresentation(block_presentation=block_presentation)


class Mutation(graphene.ObjectType):
    create_path_block_presentation = CreatePathBlockPresentation.Field()
    finish_block_presentation = FinishBlockPresentation.Field()
