from graphene import relay, ObjectType
from graphene_django import DjangoObjectType

from block.models import BlockConfigurationKeyword, BlockType, BlockTypeConfiguration, Block, BlockConfiguration, BlockPresentation, BlockQuestion, BlockQuestionPresentation

from content.models import AnswerOption, Question, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset

class BlockConfigurationKeywordType(DjangoObjectType):
    class Meta:
        model = BlockConfigurationKeyword
        fields = ('id', 'name')

class BlockTypeType(DjangoObjectType):
    class Meta:
        model = BlockType
        fields = ('id', 'name')

class BlockTypeConfigurationType(DjangoObjectType):
    class Meta:
        model = BlockTypeConfiguration
        fields = ('id', 'block_type', 'key', 'data_type', 'value')

class BlockType(DjangoObjectType):
    class Meta:
        model = Block
        fields = ('id', 'modality', 'first_presentation_timestamp', 'last_presentation_timestamp', 'type_of', 'student', 'topics', 'questions')

class BlockConfigurationType(DjangoObjectType):
    class Meta:
        model = BlockConfiguration
        fields = ('id', 'block', 'key', 'data_type', 'value')

class BlockPresentationType(DjangoObjectType):
    class Meta:
        model = BlockPresentation
        fields = ('id', 'hits', 'errors', 'total', 'points', 'start_timestamp', 'end_timestamp')

class BlockQuestionType(DjangoObjectType):
    class Meta:
        model = BlockQuestion
        fields = ('id', 'is_correct', 'is_answered', 'status')

class BlockQuestionPresentationType(DjangoObjectType):
    class Meta:
        model = BlockQuestionPresentation
        fields = ('id', 'presentation_timestamp', 'submission_timestamp', 'block_question', 'question')

class QuestionImageAssetType(DjangoObjectType):
    class Meta:
        model = QuestionImageAsset
        fields = ('image')

class QuestionAudioAssetType(DjangoObjectType):
    class Meta:
        model = QuestionAudioAsset
        fields = ('audio_file')

class QuestionVideoAssetType(DjangoObjectType):
    class Meta:
        model = QuestionVideoAsset
        fields = ('url')

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('id', 'topic', 'question_text' , 'answeroption_set', 'image_assets', 'video_assets', 'audio_assets')

class AnswerType(DjangoObjectType):
    class Meta:
        model = AnswerOption
        fields = ('id', 'answer_text', 'explanation', 'is_correct', 'question')
