from rest_framework import serializers
from .models import User
from students.serializers import StudentSerializer





class UserSerializer(serializers.ModelSerializer):
    #student_link = serializers.HyperlinkedRelatedField(view_name='api:v1:students-detail', read_only=True, lookup_field='identifier')
    student = StudentSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'student']
