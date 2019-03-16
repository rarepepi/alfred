from extension import Extension
import requests
import base64
import hmac
import json
import hashlib
import time
import config


class Gemini(Extension):
        def get_menu():
                pass

        def get_commands():
                pass

        def resolve_query():
                pass

        url = "https://api.sandbox.gemini.com"
        gemini_api_key = config.geminiTestNet['apiKey']
        gemini_api_secret = config.geminiTestNet['apiSecret'].encode('utf-8')

        def get_price(symbol):
            r = requests.get(url+"/v1/pubticker/"+symbol)
            price = r.json()
            return price['last']

        def get_btc_price():
            return get_price("btcusd")

        def get_btc_balance():
            return get_balance("BTC")

        def get_balance(symbol):
            nonce = int(time.time() * 1000)
            payload = {
                "request": "/v1/balances",
                "nonce": nonce
            }
            b64_payload = base64.b64encode(
                json.dumps(payload).encode('utf-8'))
            signature = hmac.new(
                gemini_api_secret,
                b64_payload,
                hashlib.sha384
            ).hexdigest()
            headers = {
                'Content-Type': "text/plain",
                'Content-Length': "0",
                'X-GEMINI-APIKEY': gemini_api_key,
                'X-GEMINI-PAYLOAD': b64_payload.decode('utf-8'),
                'X-GEMINI-SIGNATURE': signature,
                'Cache-Control': "no-cache"
            }

            r = requests.post(
                url+"/v1/balances",
                headers=headers)

            for balance in r.json():
                if balance['currency'] == symbol:
                    return balance['currency'] + ":" + balance['available']
