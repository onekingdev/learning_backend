from django.contrib import admin
from .models import Avatar, StudentAvatar, FavoriteAvatarCollection, AvatarPurchaseTransaction
from .resources import AvatarResource
from import_export import admin as import_export_admin


@admin.register(Avatar)
class AvatarAdmin(import_export_admin.ImportExportModelAdmin):
    resource_class = AvatarResource
    list_display = ('id', 'name', 'type_of', 'price', 'image', 'is_active')
    search_fields = ('name', 'image',)
    list_filter = ('type_of', 'price', 'is_active',)


@admin.register(StudentAvatar)
class StudentAvatarAdmin(import_export_admin.ImportExportModelAdmin):
    resource_class = AvatarResource
    list_display = ('id', 'avatar', 'student', 'in_use')
    search_fields = ('student',)
    list_filter = ('in_use',)


@admin.register(FavoriteAvatarCollection)
class FavoriteAvatarCollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'avatar_accessorie', 'avatar_head',
                    'avatar_clothes', 'avatar_pants', 'skin_tone')
    search_fields = ('student', 'avatar_accessorie', 'avatar_head', 'avatar_clothes', 'avatar_pants', 'skin_tone',)
    list_filter = ('skin_tone',)


@admin.register(AvatarPurchaseTransaction)
class AvatarPurchaseTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar')
    search_fields = ('avatar',)
    list_filter = ('avatar',)
