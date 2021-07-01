import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from content.models import AnswerOption, Question


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
