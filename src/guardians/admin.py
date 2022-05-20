from django.contrib import admin
from .models import Guardian, GuardianStudent


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'gender', 'user', 'coupon_code', 'has_order')
    search_fields = ('first_name', 'last_name', 'coupon_code', 'user',)
    list_filter = ('gender', 'has_order',)


@admin.register(GuardianStudent)
class GuardianStudent(admin.ModelAdmin):
    list_display = ('id', 'guardian', 'student')
    search_fields = ('guardian', 'student')

