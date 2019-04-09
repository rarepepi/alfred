import logging
from modules import AlfredModule
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
        print("hello world3")
        return 100


#         url = "https://api.sandbox.gemini.com"
#         gemini_api_key = config.geminiTestNet['apiKey']
#         gemini_api_secret = config.geminiTestNet['apiSecret'].encode('utf-8')

#         def get_price(symbol):
#             r = requests.get(url+"/v1/pubticker/"+symbol)
#             price = r.json()
#             return price['last']

#         def get_btc_price():
#             return get_price("btcusd")

#         def get_btc_balance():
#             return get_balance("BTC")

#         def get_balance(symbol):
#             nonce = int(time.time() * 1000)
#             payload = {
#                 "request": "/v1/balances",
#                 "nonce": nonce
#             }
#             b64_payload = base64.b64encode(
#                 json.dumps(payload).encode('utf-8'))
#             signature = hmac.new(
#                 gemini_api_secret,
#                 b64_payload,
#                 hashlib.sha384
#             ).hexdigest()
#             headers = {
#                 'Content-Type': "text/plain",
#                 'Content-Length': "0",
#                 'X-GEMINI-APIKEY': gemini_api_key,
#                 'X-GEMINI-PAYLOAD': b64_payload.decode('utf-8'),
#                 'X-GEMINI-SIGNATURE': signature,
#                 'Cache-Control': "no-cache"
#             }

#             r = requests.post(
#                 url+"/v1/balances",
#                 headers=headers)

#             for balance in r.json():
#                 if balance['currency'] == symbol:
#                     return balance['currency'] + ":" + balance['available']
