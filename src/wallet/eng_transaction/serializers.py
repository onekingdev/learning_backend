from rest_framework import serializers
from .models import EngagementTransaction

class EngagementTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = EngagementTransaction
        fields = ['id', 'name']