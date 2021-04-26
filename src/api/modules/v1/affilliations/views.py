from kb.affilliations.models import Affilliation
from kb.affilliations.serializers import AffilliationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AffilliationModule(APIView):
    """
    Retrieve, update or delete a Affilliation instance.
    """
    def get_object(self, pk):
        try:
            return Affilliation.objects.get(pk=pk)
        except Affilliation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        affilliation = self.get_object(pk)
        affilliation = AffilliationSerializer(affilliation)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        affilliation = self.get_object(pk)
        serializer = AffilliationSerializer(affilliation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        affilliation = self.get_object(pk)
        affilliation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)