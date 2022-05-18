from django.contrib import admin
from .models import SubscriptionPlan, PlanCost, GuardianSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'grace_period')
    search_fields = ('name', 'description')
    list_filter = ('grace_period',)


@admin.register(PlanCost)
class PlanCostAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan', 'recurrence_period', 'recurrence_unit', 'price')
    search_fields = ('plan__translations__name',)
    list_filter = ('plan', 'price', 'recurrence_unit', 'recurrence_period')


@admin.register(GuardianSubscription)
class GuardianSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'guardian', 'subscription', 'date_billing_start',
                    'date_billing_end', 'date_billing_last', 'date_billing_next')
    search_fields = ('guardian',)
    list_filter = ('subscription', 'date_billing_start', 'date_billing_end', 'date_billing_last', 'date_billing_next')