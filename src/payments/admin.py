from django.contrib import admin
from .models import Order, OrderDetail, PaymentHistory, PaypalTransaction, CardTransaction, PaymentMethod, DiscountCode
from import_export import admin as import_export_admin

@admin.register(PaymentMethod)
class PaymentMethodAdmin(
        import_export_admin.ImportExportModelAdmin,
):
    list_display = (
            'id',
            'guardian',
            'teacher',
            'subscriber',
            'card',
            'country',
            'phone',
            'is_default',
    )
    @admin.display(description='Card Number')
    def card(self, obj):
        str = None
        if(obj.card_number):
            card_leng = len(obj.card_number)
            first_4 = obj.card_number[0:4]
            last_4 = obj.card_number[card_leng-4:card_leng]
            str = f"{first_4} *** {last_4}"
        return str

@admin.register(CardTransaction)
class CardTransactionAdmin(
        import_export_admin.ImportExportModelAdmin,
):
    list_display = (
            'id',
            'order_detail',
            'session_id',
            'card',
            'country',
            'phone',
            'is_captured'
    )
    @admin.display(description='Card Number')
    def card(self, obj):
        str = None
        if(obj.card_number):
            card_leng = len(obj.card_number)
            first_4 = obj.card_number[0:4]
            last_4 = obj.card_number[card_leng-4:card_leng]
            str = f"{first_4} *** {last_4}"
        return str

@admin.register(DiscountCode)
class DiscountCodeAdmin(
        import_export_admin.ImportExportModelAdmin,
):
    list_display = (
            'id',
            'code',
            'percentage',
            'trial_day',
            'expired_at',
            'is_active',
    )

@admin.register(OrderDetail)
class OrderDetailAdmin(
        import_export_admin.ImportExportModelAdmin,
):
    list_display = (
            'id',
            'order',
            'plan',
            'payment_method_plan_id',
            'subscription_id',
            'quantity',
            'period',
            'total',
            'is_paid',
            'is_cancel',
    )

@admin.register(Order)
class OrderAdmin(
        import_export_admin.ImportExportModelAdmin,
):
    list_display = (
            'id',
            'guardian',
            'teacher',
            'subscriber',
            'discount_code',
            'total',
            'payment_method',
            'is_paid',
    )

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(
         import_export_admin.ImportExportModelAdmin,
):
        list_display = (
                'id',
                'type',
                'user',
                'order',
                'card',
                'amount',
                'message',
                'create_timestamp',
        )
        #--------------- Disable Editing -----------------------#
        list_display_links = None
        #--------------- Add Filter ----------------------------#
        list_filter = ('type',)
        #--------------- ADD Date Hierarcy ---------------------#
        date_hierarchy = 'create_timestamp'
        #--------------- ADD Search Field ----------------------#
        search_fields = ['user__email', 'card_number', 'type']
        #---------------#
        search_help_text = "Search by email, card number and type"

        @admin.display(description='Card Number', ordering='card_number')
        def card(self, obj):
                str = None
                if(obj.card_number):
                        card_leng = len(obj.card_number)
                        first_4 = obj.card_number[0:4]
                        last_4 = obj.card_number[card_leng-4:card_leng]
                        str = f"{first_4} *** {last_4}"
                return str

