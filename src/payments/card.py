import collections
from decimal import Decimal
from urllib.parse import urlencode

import stripe
from django.utils import timezone

from app import settings
import requests
from payments.models import CardTransaction

secret_key = settings.STRIPE_TEST_SECRET_KEY


class Card:
    token: str
    session_id: str
    url_redirect: str

    def __init__(self):
        stripe.api_key = secret_key

    def create_payment_method(self, number, exp_month, exp_year, cvc):
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc,
            },
        )
        return payment_method

    def create_customer(self, email, payment_method_id):
        customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )
        return customer

    def create_subscription(self, customer_id, plan_id, quantity, has_order, coupon_id):
        trial_day = 0
        if not has_order:
            trial_day = 7
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[
                {
                    'plan': plan_id,
                    'quantity': quantity
                },
            ],
            coupon=coupon_id,
            trial_period_days=trial_day,
            payment_behavior="error_if_incomplete"
        )
        return subscription

    def change_payment_method(self, sub_id, number, exp_month, exp_year, cvc):
        sub = stripe.Subscription.retrieve(sub_id)
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc,
            },
        )

        stripe.PaymentMethod.attach(
            payment_method.id,
            customer=sub.customer,
        )

        stripe.Customer.modify(
            sub.customer,
            invoice_settings={
                'default_payment_method': payment_method.id
            }
        )
        stripe.Subscription.modify(
            sub_id,
            default_payment_method=payment_method.id,
        )
        return

    def create_or_get_coupon(self, code, percentage):
        try:
            coupon = stripe.Coupon.create(
                duration="once",
                id=code,
                percent_off=percentage
            )
        except Exception as e:
            coupon = stripe.Coupon.retrieve(code)
        return coupon.id

    def invoice_has_paid(self, invoice_id) -> bool:
        invoice = stripe.Invoice.retrieve(invoice_id)
        if invoice.status == "paid":
            return True
        return False

    def check_subscription(self, sub_id):
        sub = stripe.Subscription.retrieve(sub_id)
        expired_at = timezone.datetime.utcfromtimestamp(int(sub.current_period_end))
        return {
            "status": sub.status,
            "expired_at": timezone.make_aware(expired_at)
        }

    def cancel_subscription(self, sub_id):
        sub = stripe.Subscription.delete(sub_id)
        return sub

    # def get_latest_invoice(self, ):
    #     return stripe.Invoice.retrieve(s.latest_invoice)

    def create_session(self, return_url: str, total: Decimal):
        url = "https://api.stripe.com/v1/checkout/sessions"
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Authorization': f'Bearer {self.token}'
        }
        params = {}
        params['cancel_url'] = return_url
        params['success_url'] = return_url
        params["line_items[0][price_data][currency]"] = "usd"
        params["line_items[0][price_data][product_data][name]"] = "Socrates Package"
        params["line_items[0][price_data][unit_amount]"] = int(total * 100)
        params["line_items[0][quantity]"] = 1
        params["mode"] = "payment"
        params["payment_method_types[0]"] = "card"
        params_ordered = collections.OrderedDict(sorted(params.items()))
        params = dict()
        for i in params_ordered:
            params[i] = params_ordered[i]

        params_encode = urlencode(params)

        response = requests.post(url=url, params=params_encode, headers=headers)
        resp = response.json()

        if response.status_code == 200:
            self.session_id = resp['id']
            self.url_redirect = resp['url']
            return
        else:
            raise Exception(resp['message'])

    def check_session(self, card_tx: CardTransaction):
        url = f'https://api.stripe.com/v1/checkout/sessions/{card_tx.session_id}'
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url=url, headers=headers)
        resp = response.json()

        if response.status_code == 200:
            if resp["payment_status"] != "paid":
                raise Exception(f'{resp["payment_status"]}')
            card_tx.is_captured = True
            card_tx.save()
        else:
            raise Exception(resp['message'])