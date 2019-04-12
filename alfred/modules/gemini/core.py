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
    def __init__(self, chat_id):
        self.name = "gemini"
        self.chat_id = chat_id
        self.commands = ['balance']
        self.base_url = "https://api.gemini.com"
        self.api_key = keys['api_key']
        self.api_secret = keys['api_secret']

    def check_auth(self, message):
        if str(message.chat_id) == self.chat_id:
            logger.info(f"User: {message.chat.username}, authenticated")
            return True
        return False
        logger.info(f"User: {message.chat.username}, failed auth")

    def resolve_query(self, query):
        # if query == "gemini-main":
        #     return self.main_menu()
        if query == "gemini-balance":
            return self.balance()

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
            query = update.callback_query.data
            text = self.resolve_query(query)
            bot.send_message(
                text=text,
                chat_id=update.callback_query.message.chat.id
            )

    def api_query(self, method, payload=None):
        if payload is None:
            payload = {}
        request_url = self.base_url + method

        payload['request'] = method
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

    def balance(self):
        response = "Asset \t | \t Amount\n --------------------------"
        r_json = self.api_query('/v1/balances')
        balances = [bal for bal in r_json if float(bal['amount']) > 0]
        for balance in balances:
            asset = balance['currency']
            amount = balance['amount']
            response = response + f"\n{asset} \t | \t {amount}"

        return response
