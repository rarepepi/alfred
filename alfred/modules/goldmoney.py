import logging
import requests
from .module import AlfredModule
from .config import goldmoney
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
        self.name = "goldmoney"
        self.menu_name = "🥇 GoldMoney"
        self.commands = [
            ('💰 Balance', "get_balance"),
        ]

    def get_balance(self):
        headers = {
            'cookie': goldmoney['cookie']
        }
        r = requests.get('https://wealth-api.goldmoney.com/balances')
        return r.json()
