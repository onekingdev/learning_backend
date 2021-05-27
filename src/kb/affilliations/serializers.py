from rest_framework import serializers
from .models import Affilliation
from kb.grades.serializers import GradeSerializer

class AffilliationSerializer(serializers.ModelSerializer):
	grade = GradeSerializer(read_only=True)
    class Meta:
        model = Affilliation
        fields = ['id', 'affilliation', 'slug', 'grade']