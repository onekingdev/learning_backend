from rest_framework import serializers
from .models import BlockConfigurationKeyword, BlockType, BlockTypeConfiguration, Block, BlockConfiguration, BlockPresentation, BlockQuestion, BlockQuestionPresentation
from content.questions.serializers import QuestionSerializer, AnswerOptionSerializer
from kb.topics.serializers import TopicSerializer
from students.serializers import StudentSerializer

class BlockConfigurationKeywordSerializer(serializers.ModelSerializer):
	class Meta:
        model = BlockConfigurationKeyword
        fields = ['id', 'name']

class BlockTypeSerializer(serializers.ModelSerializer):
	class Meta:
        model = BlockType
        fields = ['id', 'name']

class BlockTypeConfigurationSerializer(serializers.ModelSerializer):
	class Meta:
        model = BlockTypeConfiguration
        block_type = BlockConfigurationKeywordSerializer(read_only=True)
        key = BlockTypeSerializer(read_only=True)

        fields = ['id', 'block_type', 'key', 'data_type', 'value']

class BlockSerializer(serializers.ModelSerializer):
	class Meta:
        model = Block

        type_of = BlockTypeSerializer(read_only=True)
        student = StudentSerializer(many=True, read_only=True)
        topics = TopicSerializer(many=True, read_only=True)
        questions = QuestionSerializer(many=True, read_only=True)

        fields = ['id', 'modality', 'first_presentation_timestamp', 'last_presentation_timestamp', 'type_of', 'student', 'topics', 'questions']

class BlockConfigurationSerializer(serializers.ModelSerializer):
	class Meta:
        model = BlockConfiguration

		block = BlockSerializer(read_only=True)
        key = BlockConfigurationKeywordSerializer(read_only=True)

        fields = ['id', 'block', 'key', 'data_type', 'value']

class BlockPresentationSerializer(serializers.ModelSerializer):
	class Meta:
        model = BlockPresentation
        fields = ['id', 'hits', 'errors', 'total', 'points', 'start_timestamp', 'end_timestamp']

class BlockQuestionSerializer(serializers.ModelSerializer):
	class Meta:
        model = BlockQuestion

        block  = BlockSerializer(read_only=True)
		question  = QuestionSerializer(read_only=True)
		chosen_answer  = AnswerOptionSerializer(read_only=True)
        
        fields = ['id', 'is_correct', 'is_answered', 'status']

class BlockQuestionPresentationSerializer(serializers.ModelSerializer):
	class Meta:
        model = BlockQuestionPresentation

        block_question  = BlockQuestionSerializer(read_only=True)
		question  = QuestionSerializer(read_only=True)

        fields = ['id', 'presentation_timestamp', 'submission_timestamp', 'block_question', 'question']
