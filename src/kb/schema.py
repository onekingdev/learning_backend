import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from kb.models import AreaOfKnowledge, Grade, Topic, TopicGrade, Prerequisite


class AreaOfKnowledgeSchema(DjangoObjectType):
    class Meta:
        model = AreaOfKnowledge
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class GradeSchema(DjangoObjectType):
    class Meta:
        model = Grade
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class TopicSchema(DjangoObjectType):
    class Meta:
        model = Topic
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class TopicGradeSchema(DjangoObjectType):
    class Meta:
        model = TopicGrade
        fields = "__all__"


class PrerequisiteSchema(DjangoObjectType):
    class Meta:
        model = Prerequisite
        fields = "__all__"


class Query(graphene.ObjectType):
    # ----------------- AreaOfKnowledge ----------------- #

    areas_of_knowledge = graphene.List(AreaOfKnowledgeSchema)
    area_of_knowledge_by_id = graphene.Field(
        AreaOfKnowledgeSchema, id=graphene.String())

    def resolve_areas_of_knowledge(root, info, **kwargs):
        # Querying a list
        return AreaOfKnowledge.objects.all()

    def resolve_area_of_knowledge_by_id(root, info, id):
        # Querying a single question
        return AreaOfKnowledge.objects.get(pk=id)

    # ----------------- Grade ----------------- #

    grades = graphene.List(GradeSchema)
    grade = graphene.Field(GradeSchema, id=graphene.String())

    def resolve_grades(root, info, **kwargs):
        # Querying a list
        return Grade.objects.all()

    def resolve_grade(root, info, id):
        # Querying a single question
        return Grade.objects.get(pk=id)

    # ----------------- Topic ----------------- #

    topics = graphene.List(TopicSchema)
    topic_by_id = graphene.Field(TopicSchema, id=graphene.String())

    def resolve_topics(root, info, **kwargs):
        # Querying a list
        return Topic.objects.all()

    def resolve_topic_by_id(root, info, id):
        # Querying a single question
        return Topic.objects.get(pk=id)

    # ----------------- TopicGrade ----------------- #

    topics_grade = graphene.List(TopicGradeSchema)
    topic_grade_by_id = graphene.Field(TopicGradeSchema, id=graphene.String())

    def resolve_topics_grade(root, info, **kwargs):
        # Querying a list
        return TopicGrade.objects.all()

    def resolve_topic_grade_by_id(root, info, id):
        # Querying a single question
        return TopicGrade.objects.get(pk=id)

    # ----------------- Prerequisite ----------------- #

    prerequisites = graphene.List(PrerequisiteSchema)
    prerequisite_by_id = graphene.Field(
        PrerequisiteSchema, id=graphene.String())

    def resolve_prerequisites(root, info, **kwargs):
        # Querying a list
        return Prerequisite.objects.all()

    def resolve_prerequisite_by_id(root, info, id):
        # Querying a single question
        return Prerequisite.objects.get(pk=id)
