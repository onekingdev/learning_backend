from audiences.models import Audience
from audiences.serializers import AudienceSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AudienceModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return Audience.objects.get(pk=pk)
        except Audience.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        audience = self.get_object(pk)
        audience = AudienceSerializer(audience)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        audience = self.get_object(pk)
        serializer = AudienceSerializer(audience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        audience = self.get_object(pk)
        audience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)