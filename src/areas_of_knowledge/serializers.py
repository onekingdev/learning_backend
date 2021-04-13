from rest_framework import serializers
from .models import AreaOfKnowledge

class AreaOfKnowledgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AreaOfKnowledge
        fields = ['id', 'name', 'hex_color']