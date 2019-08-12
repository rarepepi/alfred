import logging
import time
import json
import base64
import hmac
import hashlib
import requests
from .module import AlfredModule
from .config import gemini_keys
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self, chat_id):
        self.name = "goldmoney"
        self.chat_id = chat_id
        self.commands = ['balance']
        self.base_url = "https://wealth-api.goldmoney.com/balances"

    def resolve_command(self, command):
        if command == "goldmoney-balance":
            return self.balance()

    def check_auth(self, message):
        if str(message.chat_id) == self.chat_id:
            logger.info(f"User: {message.chat.username}, authenticated")
            return True
        return False
        logger.info(f"User: {message.chat.username}, failed auth")

    def main_menu(self, bot, update):
        query = update.callback_query
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=f"{self.name.title()} Commands",
            reply_markup=self.module_menu_keyboard())

    def get_commands_keyboard(self):
        keyboard = []
        for command in self.commands:
            keyboard.append(
                [InlineKeyboardButton(
                    '{}'.format(command),
                    callback_data=f'{self.name}-{command}')]
                )
        keyboard.append([InlineKeyboardButton(
                    '<-- back to main',
                    callback_data='core-main')])
        return keyboard

    def module_menu_keyboard(self):
        keyboard = self.get_commands_keyboard()
        return InlineKeyboardMarkup(keyboard)

    def callback_handler(self, bot, update):
        if self.check_auth(update.callback_query.message):
            command = update.callback_query.data
            text = self.resolve_command(command)
            bot.send_message(
                text=text,
                chat_id=update.callback_query.message.chat.id
            )

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

    def balance(self):
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



headers = {
    'cookie': 
        """
        __cfduid=d3a96f68c85b382545f4ea9c517e005d41551799481; 
        PLAY_LANG=en-US; promo_code_wealth=pepitoldmetobuygold; 
        referral_code=pepitoldmetobuygold; 
        __idcontext=eyJjb29raWVJRCI6IjRZWTZUNDZWTEpQWUdVQVhYR1lTRTZMU0c0T1VUUVpKVlJOSllYV0xZNlNBPT09PSIsImRldmljZUlEIjoiNFlZNlQ0NlZMTkVLV1FZU1NHUkdHQUxVSEFRRkhaSlVTNUZaNFJNRDU2VkE9PT09IiwiaXYiOiJSVU9YTUFIVlRZTEdXTktJUUpLVFVHR0E2VT09PT09PSIsInYiOjF9; 
        __zlcmid=teiRRcIKEgVtHA; _ga=GA1.2.2040373655.1565099529; 
        goldmoney_payload=a10a9deefb988f44a9970aca6b48032e1af0a089--259556:billbezo+goldmoney@protonmail.com; 
        _gid=GA1.2.1253811765.1565448961; gmsid=cb9e90ca78b692a4422420e5ca7bda7c; _gat_UA-54330368-1=1
        """
    }