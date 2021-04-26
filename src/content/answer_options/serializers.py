from rest_framework import serializers
from .models import AnswerOption

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'is_correct', 'answer_text', 'explanation']