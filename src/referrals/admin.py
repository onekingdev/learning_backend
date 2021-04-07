from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Referral


# Register your models here.
@admin.register(Referral)
class ReferralAdmin(DraggableMPTTAdmin):
    pass
