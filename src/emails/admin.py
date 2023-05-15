from django.contrib import admin
from .models import EmailHistory, EmailTemplate, SubscriptionType, Subscription


@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'subscription_type__name')
    list_filter = ('subscription_type__name',)

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    ordering = ['name']
    
@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'success')
    search_fields = ('id', 'email_template__name')
    ordering = ['email_template__name', 'success']