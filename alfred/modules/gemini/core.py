import logging
import time
import json
import base64
import hmac
import hashlib
import requests
from ..module import AlfredModule
from .config import keys
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self):
        self.name = "gemini"
        self.commands = ['balance']
        self.url = "https://api.sandbox.gemini.com"
        self.api_key = keys['api_key']
        self.api_secret = keys['api_secret']

    def resolve_query(self, query):
        if query == "gemini-balance":
            return self.balance()

    def main_menu(self, bot, update):
        query = update.callback_query
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Commands",
            reply_markup=self.module_menu_keyboard())

    def get_commands_keyboard(self):
        keyboard = []
        for command in self.commands:
            keyboard.append(
                [InlineKeyboardButton(
                    '{}'.format(command),
                    callback_data=f'{self.name}-{command}')]
                )
        return keyboard

    def module_menu_keyboard(self):
        keyboard = self.get_commands_keyboard()
        return InlineKeyboardMarkup(keyboard)

    def callback_handler(self, bot, update):
        query = update.callback_query.data
        text = self.resolve_query(query)
        bot.send_message(
            text=text,
            chat_id=update.callback_query.message.chat.id
        )

    def balance(self):
        return 200

    def get_balance(self):
        nonce = int(time.time() * 1000)
        payload = {
            "request": "/v1/balances",
            "nonce": nonce
        }
        b64_payload = base64.b64encode(
            json.dumps(payload).encode('utf-8'))
        logger.info(f"base64: {b64_payload}")

        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            msfg=b64_payload,
            digestmode=hashlib.sha384
        ).hexdigest()
        logger.info(f"signature: {signature}")

        headers = {
            'Content-Type': "text/plain",
            'Content-Length': "0",
            'X-GEMINI-APIKEY': self.api_key,
            'X-GEMINI-PAYLOAD': b64_payload,
            'X-GEMINI-SIGNATURE': signature,
            'Cache-Control': "no-cache"
        }
        r = requests.post(
            self.url+"/v1/balances",
            headers=headers)
        print(r.json())
