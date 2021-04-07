from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404



from users.serializers import UserSerializer
from students.serializers import StudentSerializer
from assessments.serializers import AssessmentSerializer, QuestionAskedSerializer
from kb.serializers import TopicSerializer, AreaOfKnowledgeSerializer, GradeSerializer, QuestionSerializer

from students.models import Student
from kb.models import Topic, AreaOfKnowledge, Grade, Question
from assessments.models import Assessment, QuestionAsked



class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(username=self.request.user)



class StudentViewSet(viewsets.ModelViewSet):
    # lookup_field = 'identifier'
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)


class AssessmentViewSet(viewsets.ModelViewSet):
    # lookup_field = 'identifier'
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(student__user=self.request.user)


class QuestionAskedViewSet(viewsets.ModelViewSet):
    # lookup_field = 'identifier'
    queryset = QuestionAsked.objects.all()
    serializer_class = QuestionAskedSerializer


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    # lookup_field = 'identifier'
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    # permission_classes = [AllowAny]


class AreaOfKnowledgeViewSet(viewsets.ReadOnlyModelViewSet):
    # lookup_field = 'identifier'
    queryset = AreaOfKnowledge.objects.all()
    serializer_class = AreaOfKnowledgeSerializer
    permission_classes = [AllowAny]


class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    # lookup_field = 'identifier'
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [AllowAny]


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    # lookup_field = 'identifier'
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes = [AllowAny]
