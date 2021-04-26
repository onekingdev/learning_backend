from rest_framework import serializers
from .models import EngagementWallet

class EngagementWalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = EngagementWallet
        fields = ['id', 'name']