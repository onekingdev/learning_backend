from kb.topic_grades.models import TopicGrade
from kb.topic_grades.serializers import TopicGradeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TopicGradeModule(APIView):
    """
    Retrieve, update or delete a TopicGrade instance.
    """
    def get_object(self, pk):
        try:
            return TopicGrade.objects.get(pk=pk)
        except TopicGrade.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        topic_grade = self.get_object(pk)
        topic_grade = TopicGradeSerializer(topic_grade)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        topic_grade = self.get_object(pk)
        serializer = TopicGradeSerializer(topic_grade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        topic_grade = self.get_object(pk)
        topic_grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)