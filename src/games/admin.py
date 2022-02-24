from django.contrib import admin
from .models import Game, GameCategory
from parler import admin as parler_admin
from import_export.admin import ImportExportModelAdmin
from .resources import GameResource, GameCategoryResource


@admin.register(Game)
class GameAdmin(ImportExportModelAdmin, parler_admin.TranslatableAdmin):
    resource_class = GameResource


@admin.register(GameCategory)
class GameCategoryAdmin(ImportExportModelAdmin, parler_admin.TranslatableAdmin):
    resource_class = GameCategoryResource