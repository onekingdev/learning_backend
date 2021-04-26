from rest_framework import serializers
from .models import CoinWallet

class CoinWalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoinWallet
        fields = ['id', 'name']