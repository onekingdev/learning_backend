from rest_framework import serializers
from kb.questions.serializers import QuestionSerializer
from .models import Topic

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', ]


class TopicSerializer(serializers.ModelSerializer):
    topic_set = SubTopicSerializer(many=True, read_only=True)
    question_set = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'question_set', 'topic_set']