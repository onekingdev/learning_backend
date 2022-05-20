from django.contrib import admin
from .models import Interest
# Register your models here.
import random
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import BankWallet, Interest
from parler import admin as parler_admin


@admin.register(BankWallet)
class BankWalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'positive_side', 'balance')
    search_fields = ('student',)
    list_filter = ('positive_side', 'balance',)


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'period', 'requireCoin', 'amount')
    search_fields = ('name',)
    list_filter = ('period', 'requireCoin', 'amount',)
