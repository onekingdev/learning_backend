import collections
from decimal import Decimal
from urllib.parse import urlencode

import requests

from payments.models import CardTransaction

secret_key = "sk_test_51KLwL9AfwM01sssKhqb9BVSV7ATaK7ue52ryZsL8X3pyMM31KIlxN4kOLjjZFzhsgkxqHVCsvbGv1QjsHtOR0tjT00XN7EbH6d"


class Card:
    token: str
    session_id: str
    url_redirect: str

    def __init__(self):
        self.token = secret_key

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