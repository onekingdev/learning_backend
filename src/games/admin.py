from django.contrib import admin
from .models import Game, GameCategory
from parler import admin as parler_admin
from import_export.admin import ImportExportModelAdmin
from .resources import GameResource, GameCategoryResource


@admin.register(Game)
class GameAdmin(ImportExportModelAdmin, parler_admin.TranslatableAdmin):
    resource_class = GameResource
    search_fields = ('name', 'image', 'path',)
    list_filter = ('category', 'play_stats', 'cost', 'is_active',)


@admin.register(GameCategory)
class GameCategoryAdmin(ImportExportModelAdmin, parler_admin.TranslatableAdmin):
    resource_class = GameCategoryResource
    list_display = ('id', 'name', 'image', 'bg_color')
    search_fields = ('name',)
    list_filter = ('bg_color',)
