import collections
import json
from urllib.parse import urlencode
from .models import PaypalTransaction
import requests
from requests.auth import HTTPBasicAuth
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class Paypal:
    token_type: str
    access_token: str
    approve_link: str
    capture_link: str
    token_id: str

    def __init__(self):
        self.token_type = ""
        self.access_token = ""

    def get_token(self):
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        username = "AZfLPlNYc7hAb0QEh1jJxAh-WleJvAIqBeI0ZhPKSjX-2z9Q_1hAveZ0i4Do7rX29tus9XRidtDFivA9"
        password = "EOoTJHQZsLretu2Zh2wd0WoDXwP8BuJCrD5vYHxKpgBoC4_SzvOi_N9VipMmbHly1VphZh5TAEMJ6VVP"
        basic_auth = HTTPBasicAuth(username, password)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'
        }
        params = {}
        params['grant_type'] = "client_credentials"
        params_ordered = collections.OrderedDict(sorted(params.items()))
        params = dict()
        for i in params_ordered:
            params[i] = params_ordered[i]

        params_encode = urlencode(params)

        response = requests.post(url=url, params=params_encode, auth=basic_auth, headers=headers)
        resp = response.json()

        if response.status_code == 200:
            self.token_type = resp['token_type']
            self.access_token = resp['access_token']
        else:
            raise Exception("Cannot get token paypal.")

    def check_out(self, return_url, cancel_url, value):
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        headers = {
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': f'{self.token_type} {self.access_token}'
        }
        body = dict()
        body['intent'] = 'CAPTURE'
        body['application_context'] = {
            "return_url": return_url,
            "cancel_url": cancel_url
        }
        body['purchase_units'] = [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": value
                }
            }
        ]

        data_to_json = json.dumps(body, indent=4, cls=DecimalEncoder)
        response = requests.post(url=url, data=data_to_json, headers=headers)
        resp = response.json()

        if response.status_code == 201:
            self.token_id = resp["id"]
            for link in resp["links"]:
                if link["rel"] == "approve":
                    self.approve_link = link["href"]
                elif link["rel"] == "capture":
                    self.capture_link = link["href"]
            return
        else:
            raise Exception("Cannot create checkout paypal.")

    def capture(self, paypal_tx: PaypalTransaction):
        url = paypal_tx.capture_link
        headers = {
            'Content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': f'{self.token_type} {self.access_token}'
        }
        body = dict()
        data_to_json = json.dumps(body, indent=4, cls=DecimalEncoder)
        response = requests.post(url=url, data=data_to_json, headers=headers)
        resp = response.json()

        if response.status_code == 201:
            if resp["status"] != "COMPLETED":
                raise Exception(f'{resp["status"]}')
            paypal_tx.is_captured = True
            paypal_tx.save()
        else:
            raise Exception("Cannot capture checkout paypal.")