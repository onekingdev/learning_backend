from block.models import BlockConfigurationKeyword, BlockType, BlockTypeConfiguration, Block, BlockConfiguration, BlockPresentation, BlockQuestion, BlockQuestionPresentation
from block.serializers import BlockConfigurationKeywordSerializer, BlockTypeSerializer, BlockTypeConfigurationSerializer, BlockSerializer, BlockConfigurationSerializer, BlockPresentationSerializer, BlockQuestionSerializer, BlockQuestionPresentationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BlockConfigurationKeywordModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return BlockConfigurationKeyword.objects.get(pk=pk)
        except BlockConfigurationKeyword.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        block_configuration_keyword = self.get_object(pk)
        block_configuration_keyword = BlockConfigurationKeywordSerializer(block_configuration_keyword)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        block_configuration_keyword = self.get_object(pk)
        serializer = BlockConfigurationKeywordSerializer(block_configuration_keyword, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        block_configuration_keyword = self.get_object(pk)
        block_configuration_keyword.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlockTypeModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return BlockType.objects.get(pk=pk)
        except BlockType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        block_type = self.get_object(pk)
        block_type = BlockTypeSerializer(block_type)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        block_type = self.get_object(pk)
        serializer = BlockTypeSerializer(block_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        block_type = self.get_object(pk)
        block_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlockTypeConfigurationModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return BlockTypeConfiguration.objects.get(pk=pk)
        except BlockTypeConfiguration.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        block_type_configuration = self.get_object(pk)
        block_type_configuration = BlockTypeConfigurationSerializer(block_type_configuration)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        block_type_configuration = self.get_object(pk)
        serializer = BlockTypeConfigurationSerializer(block_type_configuration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        block_type_configuration = self.get_object(pk)
        block_type_configuration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlockModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return Block.objects.get(pk=pk)
        except Block.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        block = self.get_object(pk)
        block = BlockSerializer(block)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        block = self.get_object(pk)
        serializer = BlockSerializer(block, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        block = self.get_object(pk)
        block.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlockConfigurationModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return BlockConfiguration.objects.get(pk=pk)
        except BlockConfiguration.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        block_configuration = self.get_object(pk)
        block_configuration = BlockConfigurationSerializer(block_configuration)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        block_configuration = self.get_object(pk)
        serializer = BlockConfigurationSerializer(block_configuration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        block_configuration = self.get_object(pk)
        block_configuration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlockPresentationModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return BlockPresentation.objects.get(pk=pk)
        except BlockPresentation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        block_presentation = self.get_object(pk)
        block_presentation = BlockPresentationSerializer(block_presentation)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        block_presentation = self.get_object(pk)
        serializer = BlockPresentationSerializer(block_presentation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        block_presentation = self.get_object(pk)
        block_presentation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlockQuestionModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return BlockQuestion.objects.get(pk=pk)
        except BlockQuestion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        block_question = self.get_object(pk)
        block_question = BlockQuestionSerializer(block_question)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        block_question = self.get_object(pk)
        serializer = BlockQuestionSerializer(block_question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        block_question = self.get_object(pk)
        block_question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlockQuestionPresentationModule(APIView):
    """
    Retrieve, update or delete a Topic instance.
    """
    def get_object(self, pk):
        try:
            return BlockQuestionPresentation.objects.get(pk=pk)
        except BlockQuestionPresentation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        block_question_presentation = self.get_object(pk)
        block_question_presentation = BlockQuestionPresentationSerializer(block_question_presentation)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        block_question_presentation = self.get_object(pk)
        serializer = BlockQuestionPresentationSerializer(block_question_presentation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        block_question_presentation = self.get_object(pk)
        block_question_presentation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)