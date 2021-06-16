from django.contrib import admin
from .models import BlockType
from parler import admin as parler_admin



# Register your models here.
@admin.register(BlockType)
class BlockTypeAdmin(parler_admin.TranslatableAdmin):
    pass

