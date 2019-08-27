import logging
import time
import json
import base64
import hmac
import hashlib
import requests
from .module import AlfredModule
from .config import gemini

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self):
        self.name = "gemini"
        self.menu_name = "📟 Gemini"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]
        self.base_url = "https://api.gemini.com/v1"
        self.api_key = gemini['api_key']
        self.api_secret = gemini['api_secret']

    def private_api_query(self, method, payload=None):
        if payload is None:
            payload = {}
        request_url = self.base_url + method

        payload['request'] = '/v1' + method
        payload['nonce'] = int(time.time() * 1000)
        b64_payload = base64.b64encode(
            json.dumps(payload).encode('utf-8'))

        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            b64_payload,
            hashlib.sha384,
        ).hexdigest()

        headers = {
            'Content-Type': "text/plain",
            'Content-Length': "0",
            'X-GEMINI-APIKEY': self.api_key,
            'X-GEMINI-PAYLOAD': b64_payload,
            'X-GEMINI-SIGNATURE': signature,
            'Cache-Control': "no-cache"
        }

        r = requests.post(
            request_url,
            headers=headers)
        return r.json()

    def public_api_query(self, method, payload=None):
        if payload is None:
            payload = {}
        request_url = self.base_url + method

        r = requests.get(request_url)
        return r.json()

    def price(self, asset):
        ticker = self.public_api_query(f'/pubticker/{asset.lower()}usd')
        return float(ticker['last'])

    def get_balance_detailed(self):
        response = "Asset\t|\tAmount@Price\t|\tUSD\n-----------------------------"
        r_json = self.private_api_query('/balances')
        balances = [bal for bal in r_json if float(bal['amount']) > 0]
        total_usd = 0
        for balance in balances:
            asset = balance['currency']
            amount = round(float(balance['amount']), 5)
            if asset == "USD":
                price = 1
            else:
                price = self.price(asset)
            usd_value = round(price * amount, 2)
            total_usd += usd_value
            response = response + f"\n{asset}\t|\t{amount}@{price}\t|\t{usd_value}"
        response = response + f"\n\nTotal: ${round(total_usd, 2)}"
        return response
