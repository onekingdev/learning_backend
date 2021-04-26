from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableModelForm, TranslatableTabularInline, TranslatableStackedInline
from .models import CointWallet
from import_export.admin import ImportExportModelAdmin

@admin.register(CointWallet)
class CointWalletAdmin(TranslatableAdmin):
    pass
