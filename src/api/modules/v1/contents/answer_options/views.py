from content.questions.models import AnswerOption
from content.questions.serializers import AnswerOptionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TopicModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return AnswerOption.objects.get(pk=pk)
        except AnswerOption.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        answer_option = self.get_object(pk)
        answer_option = AnswerOptionSerializer(answer_option)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        answer_option = self.get_object(pk)
        serializer = AnswerOptionSerializer(answer_option, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        answer_option = self.get_object(pk)
        answer_option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)