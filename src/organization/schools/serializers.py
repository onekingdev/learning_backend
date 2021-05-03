from rest_framework import serializers
from .models import School, Group, SchoolPersonnel

from users.serializers import UserSerializer
from students.serializers import StudentSerializer
from organization.org.serializers import OrganizationSerializer
from kb.grades.serializers import GradeSerializer
from kb.area_of_knowledges.serializers import AreaOfKnowledgeSerializer

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        grade  = GradeSerializer(read_only=True)
		area_of_knowledges = AreaOfKnowledgeSerializer(many=True, read_only=True)

        fields = ['id', 'name', 'internal_code', 'population', 'grade', 'area_of_knowledges']

class SchoolPersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolPersonnel
        user = UserSerializer(read_only=True)
		school = SchoolSerializer(read_only=True)

        fields = ['id', 'name', 'last_name', 'gender', 'date_of_birth', 'identification_number', 'position', 'user', 'school']


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School

        organization = OrganizationSerializer(read_only=True)
		teacher = SchoolPersonnelSerializer(many=True, read_only=True)
		student = StudentSerializer(many=True, read_only=True)
		group = GroupSerializer(many=True, read_only=True)

        fields = ['id', 'name', 'slug', 'internal_code', 'type_of', 'organization', 'teacher', 'student', 'group']
