from django.db import models
from app.models import TimestampModel


class TopicMasterySettings(models.Model):
    topic = models.ForeignKey(
        'kb.Topic',
        on_delete=models.CASCADE,
        related_name='values'
    )
    sample_size = models.IntegerField(default=50)
    mastery_percentage = models.IntegerField(default=90)
    competence_percentage = models.IntegerField(default=60)


class TopicStudentReport(TimestampModel):
    topic = models.ForeignKey('kb.Topic', on_delete=models.PROTECT)
    student = models.ForeignKey('students.Student', on_delete=models.PROTECT)
    questions_answered = models.IntegerField(default=0)
    correct_question = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)


class AreaOfKnowledgeStudentReport(TimestampModel):
    area_of_knowledge = models.ForeignKey(
        'kb.AreaOfKnowledge',
        on_delete=models.PROTECT
    )
    student = models.ForeignKey('students.Student', on_delete=models.PROTECT)
    questions_answered = models.IntegerField(default=0)
    correct_question = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)
