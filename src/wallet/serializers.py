from rest_framework import serializers
from .models import TypeTransaction, Wallet, Transaction, PaymentOption, Invoice

class TypeTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeTransaction
        fields = ['id', 'name']

class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['id', 'user']

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'amount', 'type_transaction', 'format_transaction', 'notes']

class PaymentOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentOption
        fields = ['id', 'name', 'dollar_amount', 'wallet_amount', 'enabled']

class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['id', 'user', 'option', 'date_billed', 'transaction']
        