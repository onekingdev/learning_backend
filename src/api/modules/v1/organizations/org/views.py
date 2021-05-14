from organization.org.models import Organization, OrganizationPersonnel
from organization.org.serializers import OrganizationSerializer, OrganizationPersonnelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class OrganizationModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        organization = self.get_object(pk)
        organization = OrganizationSerializer(organization)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        organization = self.get_object(pk)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrganizationPersonnelModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return OrganizationPersonnel.objects.get(pk=pk)
        except OrganizationPersonnel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        organization_personnel = self.get_object(pk)
        organization_personnel = OrganizationPersonnelSerializer(organization_personnel)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        organization_personnel = self.get_object(pk)
        serializer = OrganizationPersonnelSerializer(organization_personnel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        organization_personnel = self.get_object(pk)
        organization_personnel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)