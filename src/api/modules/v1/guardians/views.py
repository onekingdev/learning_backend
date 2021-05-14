from guardians.models import Guardian, GuardianStudent
from guardians.serializers import GuardianSerializer, GuardianStudentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GuardianModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return Guardian.objects.get(pk=pk)
        except Guardian.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        guardian = self.get_object(pk)
        guardian = GuardianSerializer(guardian)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        guardian = self.get_object(pk)
        serializer = GuardianSerializer(guardian, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        guardian = self.get_object(pk)
        guardian.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GuardianStudentModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return GuardianStudent.objects.get(pk=pk)
        except GuardianStudent.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        guardian_student = self.get_object(pk)
        guardian_student = GuardianStudentSerializer(guardian_student)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        guardian_student = self.get_object(pk)
        serializer = GuardianStudentSerializer(guardian_student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        guardian_student = self.get_object(pk)
        guardian_student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)