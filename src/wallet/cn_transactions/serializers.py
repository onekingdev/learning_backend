from rest_framework import serializers
from .models import CoinTransaction

class CoinTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoinTransaction
        fields = ['id', 'name']