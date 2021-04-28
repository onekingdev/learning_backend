from rest_framework import serializers
from .models import School, Group

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'name']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']
