from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'street', 'ext_no', 'int_no', 'city', 'zip', 'state', 'country', 'type']