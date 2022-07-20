import graphene
from graphene_django import DjangoObjectType
from .models import Notes


class NotesSchema(DjangoObjectType):
    class Meta:
        model = Notes
        fields = "__all__"

class Query(graphene.ObjectType):
    # ----------------- Organization ----------------- #

    notes = graphene.List(NotesSchema)
    notes_by_id = graphene.Field(
        NotesSchema, id=graphene.String())

    def resolve_organizations(root, info, **kwargs):
        # Querying a list
        return Notes.objects.all()

    def resolve_organization_by_id(root, info, id):
        # Querying a single question
        return Notes.objects.get(pk=id)

