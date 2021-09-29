from import_export.resources import ModelResource
from .models import Student


class TopicAdminResource(ModelResource):
    class Meta:
        model = Topic
        fields = ['first_name', 'last_name']


