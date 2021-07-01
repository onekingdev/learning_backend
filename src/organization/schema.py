import graphene
from graphene_django import DjangoObjectType
from organization.models import Organization, OrganizationPersonnel, Group, School, SchoolPersonnel


class OrganizationSchema(DjangoObjectType):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationPersonnelSchema(DjangoObjectType):
    class Meta:
        model = OrganizationPersonnel
        fields = "__all__"


class GroupSchema(DjangoObjectType):
    class Meta:
        model = Group
        fields = "__all__"


class SchoolSchema(DjangoObjectType):
    class Meta:
        model = School
        fields = "__all__"


class SchoolPersonnelSchema(DjangoObjectType):
    class Meta:
        model = SchoolPersonnel
        fields = "__all__"


class Query(graphene.ObjectType):
    # ----------------- Organization ----------------- #

    organizations = graphene.List(OrganizationSchema)
    organization_by_id = graphene.Field(
        OrganizationSchema, id=graphene.String())

    def resolve_organizations(root, info, **kwargs):
        # Querying a list
        return Organization.objects.all()

    def resolve_organization_by_id(root, info, id):
        # Querying a single question
        return Organization.objects.get(pk=id)

    # ----------------- OrganizationPersonnel ----------------- #

    organizations_personnel = graphene.List(OrganizationPersonnelSchema)
    organization_personnel_by_id = graphene.Field(
        OrganizationPersonnelSchema, id=graphene.String())

    def resolve_organizations_personnel(root, info, **kwargs):
        # Querying a list
        return OrganizationPersonnel.objects.all()

    def resolve_organization_personnel_by_id(root, info, id):
        # Querying a single question
        return OrganizationPersonnel.objects.get(pk=id)

    # ----------------- Group ----------------- #

    groups = graphene.List(GroupSchema)
    group_by_id = graphene.Field(GroupSchema, id=graphene.String())

    def resolve_groups(root, info, **kwargs):
        # Querying a list
        return Group.objects.all()

    def resolve_group_by_id(root, info, id):
        # Querying a single question
        return Group.objects.get(pk=id)

    # ----------------- School ----------------- #

    schools = graphene.List(SchoolSchema)
    school_by_id = graphene.Field(SchoolSchema, id=graphene.String())

    def resolve_schools(root, info, **kwargs):
        # Querying a list
        return School.objects.all()

    def resolve_school_by_id(root, info, id):
        # Querying a single question
        return School.objects.get(pk=id)

    # ----------------- SchoolPersonnel ----------------- #

    schools_personnel = graphene.List(SchoolPersonnelSchema)
    school_personnel_by_id = graphene.Field(
        SchoolPersonnelSchema, id=graphene.String())

    def resolve_schools_personnel(root, info, **kwargs):
        # Querying a list
        return SchoolPersonnel.objects.all()

    def resolve_school_personnel_by_id(root, info, id):
        # Querying a single question
        return SchoolPersonnel.objects.get(pk=id)
