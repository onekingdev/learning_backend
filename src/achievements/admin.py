from django.contrib import admin
from .models import Achievement
from parler import admin as parler_admin


@admin.register(Achievement)
class AchievementAdmin(parler_admin.TranslatableAdmin):
    list_display = ('id', 'name', 'slug', 'image', 'hex_color', 'level_required',
                    'engangement_points', 'coins_earned', 'is_active')
    search_fields = ('name', 'positive_side',)
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ('id', 'slug', 'level_required', 'engangement_points', 'coins_earned', 'is_active')
    fieldsets = ()
