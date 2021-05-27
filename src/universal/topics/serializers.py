from rest_framework import serializers
from universal.area_of_knowledges.serializers import AreaOfKnowledgeSerializer
from .models import Topic

class SubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', ]


class TopicSerializer(serializers.ModelSerializer):
    area_of_knowledge = AreaOfKnowledgeSerializer(read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'standard_code', 'parent', 'area_of_knowledge']