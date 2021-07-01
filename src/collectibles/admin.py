from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableModelForm
from mptt.admin import DraggableMPTTAdmin
from mptt.forms import MPTTAdminForm
from .models import CollectibleCategory, Collectible


class CollectibleCategoryForm(MPTTAdminForm, TranslatableModelForm):
    pass


@admin.register(CollectibleCategory)
class CollectibleCategoryAdmin(TranslatableAdmin, DraggableMPTTAdmin):
    form = CollectibleCategoryForm

    def get_prepopulated_fields(self, request, obj=None):
        return {'name': ('description',)}


@admin.register(Collectible)
class CollectibleAdmin(TranslatableAdmin):
    pass
