from rest_framework import serializers
from .models import Guardian, GuardianStudent
from users.serializers import UserSerializer
from students.serializers import StudentSerializer

class GuardianSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guardian
        user  = UserSerializer(read_only=True)
        fields = ['id', 'name', 'last_name', 'gender', 'user']

class GuardianStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuardianStudent
        guardian  = GuardianSerializer(read_only=True)
        student  = StudentSerializer(read_only=True)

        fields = ['id', 'guardian', 'student']