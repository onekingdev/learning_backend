from organization.schools.models import Group, School, SchoolPersonnel, AdministrativePersonnel, Teacher
from organization.schools.serializers import GroupSerializer, SchoolPersonnelSerializer, AdministrativePersonnelSerializer, TeacherSerializer, SchoolSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class GroupModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        group = self.get_object(pk)
        group = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SchoolModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return School.objects.get(pk=pk)
        except School.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        school = self.get_object(pk)
        school = SchoolSerializer(school)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        school = self.get_object(pk)
        serializer = SchoolSerializer(school, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        school = self.get_object(pk)
        school.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SchoolPersonnelModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return SchoolPersonnel.objects.get(pk=pk)
        except SchoolPersonnel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        school_personnel = self.get_object(pk)
        school_personnel = SchoolPersonnelSerializer(school_personnel)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        school_personnel = self.get_object(pk)
        serializer = SchoolPersonnelSerializer(school_personnel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        school_personnel = self.get_object(pk)
        school_personnel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdministrativePersonnelModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return AdministrativePersonnel.objects.get(pk=pk)
        except AdministrativePersonnel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        administrative_personnel = self.get_object(pk)
        administrative_personnel = AdministrativePersonnelSerializer(administrative_personnel)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        administrative_personnel = self.get_object(pk)
        serializer = AdministrativePersonnelSerializer(administrative_personnel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        administrative_personnel = self.get_object(pk)
        administrative_personnel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TeacherModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        teacher = self.get_object(pk)
        teacher = TeacherSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        teacher = self.get_object(pk)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)