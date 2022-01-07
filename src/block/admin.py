from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import BlockType, BlockAssignment
from parler import admin as parler_admin


# Register your models here.
@admin.register(BlockType)
class BlockTypeAdmin(parler_admin.TranslatableAdmin):
    pass


@admin.register(BlockAssignment)
class BlockAssignmentAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass
