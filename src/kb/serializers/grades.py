from rest_framework import serializers
from .models import Grade
from audiences.serializers import AudienceSerializer

class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        audience  = AudienceSerializer(read_only=True)

        fields = ['id', 'name', 'slug', 'audience']