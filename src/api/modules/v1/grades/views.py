from kb.grades.models import Grade
from kb.grades.serializers import GradeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GradeModule(APIView):
    """
    Retrieve, update or delete a Grade instance.
    """
    def get_object(self, pk):
        try:
            return Grade.objects.get(pk=pk)
        except Grade.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        grade = self.get_object(pk)
        grade = GradeSerializer(grade)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        grade = self.get_object(pk)
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        grade = self.get_object(pk)
        grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)