from rest_framework import serializers
from .models import TopicGrade
from kb.grades.serializers import GradeSerializer

class TopicGradeSerializer(serializers.ModelSerializer):
	grade = GradeSerializer(read_only=True)
    class Meta:
        model = TopicGrade
        fields = ['id', 'year_point', 'slug', 'grade']