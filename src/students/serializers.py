from rest_framework import serializers
from .models import Student
from assessments.serializers import AssessmentSerializer
from kb.serializers import GradeSerializer, AreaOfKnowledgeSerializer

class StudentSerializer(serializers.ModelSerializer):
    assessment_set = AssessmentSerializer(many=True, read_only=True)
    # grade = GradeSerializer(read_only=True)
    pending_aok = serializers.SerializerMethodField('get_pending_aok')

    def get_pending_aok(self, obj):
        qs = obj.get_pending_assessment_area_of_knowledge_set()
        serializer = AreaOfKnowledgeSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Student
        fields = ['id','user', 'grade', 'first_name', 'last_name',  'assessment_set', 'pending_aok']
