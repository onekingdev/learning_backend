from kb.area_of_knowledges.models import AreaOfKnowledge
from kb.area_of_knowledges.serializers import AreaOfKnowledgeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AreaOfKnowledgeModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return AreaOfKnowledge.objects.get(pk=pk)
        except AreaOfKnowledge.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        area_of_knowledge = self.get_object(pk)
        area_of_knowledge = AreaOfKnowledgeSerializer(area_of_knowledge)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        area_of_knowledge = self.get_object(pk)
        serializer = AreaOfKnowledgeSerializer(area_of_knowledge, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        area_of_knowledge = self.get_object(pk)
        area_of_knowledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)