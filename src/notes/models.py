from django.db import models
from app.models import RandomSlugModel, TimestampModel, IsActiveModel
from organization.models.schools import Teacher
from students.models import Student
class Notes(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'notes_'
    title = models.CharField(max_length=64, null=False)
    text = models.TextField(null=True)
    send_at = models.DateTimeField(editable=True, null=True, blank=True )
    user_from = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='note_sent',
        null=True,
        blank=True
    )
    user_to = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='note_received',
        null=True,
        blank=True
    )