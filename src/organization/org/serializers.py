from rest_framework import serializers
from .models import Organization, OrganizationPersonnel
from users.serializers import UserSerializer

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'name', 'type_of', 'slug', 'parent']

class OrganizationPersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationPersonnel

        user = UserSerializer(read_only=True)
		organization = OrganizationSerializer(read_only=True)

        fields = ['id', 'name', 'last_name', 'gender', 'date_of_birth', 'identification_number', 'position', 'user', 'organization']







