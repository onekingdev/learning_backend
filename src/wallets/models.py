from django.utils.text import slugify
from django.db import models, connection

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from app.models import RandomSlugModel, TimestampModel, UUIDModel, IsActiveModel

# Create your models here.
class TypeTransaction(TimestampModel, RandomSlugModel, IsActiveModel, TranslatableModel):
    PREFIX = 'typ_trns_'
    name  = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name

class Wallet(TimestampModel, RandomSlugModel, IsActiveModel):
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, unique=True, related_name='wallets')
    
    #class Meta:
        #permissions = (('can_view_wallet_report', 'Can view wallet report'),)
    
    def __unicode__(self):
        return "%s's wallet" % self.user.username
    
    def get_balance(self):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) FROM wallet_transaction WHERE wallet_id = %s",
            (self.id,)
        )
        value = cursor.fetchone()[0]
        if value is None:
            value = Decimal('0.0')
        return value
    
    def withdraw(self, value, allow_overdraft=False):
        if not isinstance(value, int) and not isinstance(value, Decimal):
            raise ValueError("Value must be a Python int or Decimal")
        if value < 0:
            raise ValueError("You can't withdraw a negative amount")
        if not allow_overdraft and (self.get_balance() - value) < 0:
            raise Overdraft
        return self.transactions.create(
            date=datetime.datetime.now(),
            value=value * Decimal('-1.0'),
        )
    
    def deposit(self, value):
        if not isinstance(value, int) and not isinstance(value, Decimal):
            raise ValueError("Value must be a Python int or Decimal")
        if value < 0:
            raise ValueError("You can't deposit a negative amount")
        return self.transactions.create(
            date=datetime.datetime.now(),
            value=value,
        )


class Transaction(TimestampModel, RandomSlugModel, UUIDModel, IsActiveModel, TranslatableModel):
    date = models.DateTimeField(blank=True)
    amount = models.FloatField(max_length=20,blank=True)
    type_transaction = models.ForeignKey('wallets.TypeTransaction', on_delete=models.PROTECT, null=True)
    format_transaction = models.CharField(max_length=128, null=True)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return 'Transaction #%d (%.2f)' % (self.id, self.value)

class PaymentOption(TimestampModel, RandomSlugModel, IsActiveModel):
    name = models.CharField(max_length=255)
    dollar_amount = models.FloatField(max_length=20,blank=True)
    wallet_amount = models.FloatField(max_length=20,blank=True)
    enabled = models.BooleanField(default=True)
    
    def __unicode__(self):
        return '%s ($%.2f)' % (self.name, self.dollar_amount)

class Invoice(TimestampModel, RandomSlugModel, IsActiveModel):
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='wallet_invoices')
    option = models.ForeignKey('wallets.PaymentOption', on_delete=models.PROTECT, related_name='invoices')
    date_billed = models.DateTimeField()
    transaction = models.ForeignKey(
        'wallets.Transaction',
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,
        blank=True,
        unique=True,
    )