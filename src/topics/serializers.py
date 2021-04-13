from rest_framework import serializers
from questions import serializers as QSerializer
from .models import Topic

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', ]


class TopicSerializer(serializers.ModelSerializer):
    topic_set = SubTopicSerializer(many=True, read_only=True)
    question_set = QSerializer.QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'question_set', 'topic_set']