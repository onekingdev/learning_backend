from rest_framework import serializers
from .models import Personnel

class PersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personnel
        fields = ['id', 'name']