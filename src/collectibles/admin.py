from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableModelForm
from mptt.admin import DraggableMPTTAdmin
from mptt.forms import MPTTAdminForm
from .models import CollectibleCategory, Collectible, CollectiblePurchaseTransaction, StudentCollectible, \
    CollectiblePackPurchaseTransaction
from .models import Description, CollectibleDescription
from import_export import admin as import_export_admin
from .resources import CollectibleResource, DescriptionResource, CollectibleDescriptionResource


@admin.action(description='Hard delete objects')
def hard_delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.hard_delete()


class CollectibleCategoryForm(MPTTAdminForm, TranslatableModelForm):
    pass


@admin.register(CollectibleCategory)
class CollectibleCategoryAdmin(TranslatableAdmin, DraggableMPTTAdmin):
    form = CollectibleCategoryForm
    list_display = ('indented_title', 'description', 'parent', 'front_image', 'back_image', 'price', 'firebase_name')
    search_fields = ('indented_title', 'description', 'parent',)
    list_filter = ('price',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'name': ('description',)}


@admin.register(Collectible)
class CollectibleAdmin(TranslatableAdmin, import_export_admin.ImportExportModelAdmin):
    resource_class = CollectibleResource
    list_display = ('id', 'name', 'image', 'category', 'tier')
    search_fields = ('name',)
    list_filter = ('category', 'tier',)


@admin.register(Description)
class DescriptionAdmin(TranslatableAdmin, import_export_admin.ImportExportModelAdmin):
    resource_class = DescriptionResource
    list_display = ('id', 'key', 'value')
    search_fields = ('key', 'value',)


@admin.register(CollectibleDescription)
class CollectibleDescriptionAdmin(import_export_admin.ImportExportModelAdmin):
    resource_class = CollectibleDescriptionResource
    list_display = ('id', 'collectible_id', 'description_id')
    search_fields = ('collectible', 'description',)


@admin.register(CollectiblePurchaseTransaction)
class CollectiblePurchaseTransactionAdmin(admin.ModelAdmin):
    exclude = ('amount',)
    list_display = ('id', 'account', 'side', 'comment', 'amount', 'collectible', 'date')
    search_fields = ('account', 'comment',)
    list_filter = ('side', 'side', 'collectible', 'date',)


@admin.register(StudentCollectible)
class StudentCollectibleAdmin(admin.ModelAdmin):
    list_display = ('id', 'collectible', 'student', 'amount', 'is_active')
    search_fields = ('collectible', 'student',)
    list_filter = ('amount', 'is_active',)
    actions = [hard_delete_selected]


@admin.register(CollectiblePackPurchaseTransaction)
class CollectiblePackPurchaseTransactionAdmin(admin.ModelAdmin):
    search_fields = ('collectible_category',)
    list_filter = ('collectible_category',)
