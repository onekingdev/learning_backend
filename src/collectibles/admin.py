from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableModelForm
from mptt.admin import DraggableMPTTAdmin
from mptt.forms import MPTTAdminForm
from .models import CollectibleCategory, Collectible, CollectiblePurchaseTransaction, StudentCollectible
from import_export import admin as import_export_admin
from .resources import CollectibleResource


@admin.action(description='Hard delete objects')
def hard_delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.hard_delete()


class CollectibleCategoryForm(MPTTAdminForm, TranslatableModelForm):
    pass


@admin.register(CollectibleCategory)
class CollectibleCategoryAdmin(TranslatableAdmin, DraggableMPTTAdmin):
    form = CollectibleCategoryForm

    def get_prepopulated_fields(self, request, obj=None):
        return {'name': ('description',)}


@admin.register(Collectible)
class CollectibleAdmin(
        TranslatableAdmin,
        import_export_admin.ImportExportModelAdmin):
    resource_class = CollectibleResource


@admin.register(CollectiblePurchaseTransaction)
class CollectiblePurchaseTransactionAdmin(admin.ModelAdmin):
    exclude = ('amount',)
    list_display = ('collectible', 'account', 'amount', 'date')


@admin.register(StudentCollectible)
class StudentCollectibleAdmin(admin.ModelAdmin):
    list_display = ('collectible', 'student', 'amount')
    actions = [hard_delete_selected]
