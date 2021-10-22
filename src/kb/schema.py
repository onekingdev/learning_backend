import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from kb.models import AreaOfKnowledge, Grade, Topic, TopicGrade, Prerequisite
from kb.models.content import Question, AnswerOption


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


class QuestionSchema(DjangoObjectType):
    class Meta:
        model = Question
        fields = "__all__"

    question_text = graphene.String()

    def resolve_question_text(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("question_text", language_code=current_language)


class AnswerOptionSchema(DjangoObjectType):
    class Meta:
        model = AnswerOption
        fields = "__all__"

    answer_text = graphene.String()
    explanation = graphene.String()
    image = graphene.String()
    audio_file = graphene.String()
    video = graphene.String()

    def resolve_answer_text(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("answer_text", language_code=current_language)

    def resolve_image(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("image", language_code=current_language)

    def resolve_explanation(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("explanation", language_code=current_language)

    def resolve_audio_file(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("audio_file", language_code=current_language)

    def resolve_video(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("video", language_code=current_language)


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

    # ----------------- Question ----------------- #

    questions = graphene.List(QuestionSchema)
    question_by_id = graphene.Field(QuestionSchema, id=graphene.String())

    def resolve_questions(root, info, **kwargs):
        # Querying a list
        return Question.objects.all()

    def resolve_question_by_id(root, info, id):
        # Querying a single question
        return Question.objects.get(pk=id)

    # ----------------- AnswerOption ----------------- #

    answers_option = graphene.List(AnswerOptionSchema)
    answers_option_by_id = graphene.Field(
        AnswerOptionSchema, id=graphene.String())

    def resolve_answers_option(root, info, **kwargs):
        # Querying a list
        return AnswerOption.objects.all()

    def resolve_answers_option_by_id(root, info, id):
        # Querying a single question
        return AnswerOption.objects.get(pk=id)
