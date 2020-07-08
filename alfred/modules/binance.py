from binance.client import Client

import logging

from modules.module import AlfredModule
from modules.configs.config import binance

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self):
        self.name = "binance"
        self.menu_name = "🤑 Binance"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]
        self.client = Client(binance['api_key'], binance['secret_key'])

    def get_balance_detailed(self):
        account = self.client.get_account()

        # Filter out balances less than 0.00003
        balances = [balance for balance in account['balances'] if float(balance['free']) > 0.00003]

        current_btc_price = self.client.get_avg_price(symbol='BTCUSDT')
        total_usd = 0
        balance_detailed_str = "-----------------------------------------\n"

        # Go through all of the asset balances and add up their values
        for balance in balances:
            # Try to get price of asset in USDT
            try:
                price_in_usdt = self.client.get_avg_price(symbol=f"{balance['asset']}USDT")['price']
            except:
                # Attempt again to get price in BTC instead, and convert to USDT
                try:
                    price_in_btc = self.client.get_avg_price(symbol=f"{balance['asset']}BTC")['price']
                    price_in_usdt = price_in_btc * current_btc_price
                except:
                    price_in_usdt = 0
            total_usd += float(price_in_usdt) * float(balance['free'])
            balance_detailed_str += f"💰[ {round(float(balance['free']), 5)} ] | {balance['asset']} | ${price_in_usdt}\n"

        balance_detailed_str += "---------------------------------------------\n"
        balance_detailed_str += f"Total Binance Holdings: ${round(total_usd, 2)}\n"
        balance_detailed_str += "------------------------------------------------\n"

        return balance_detailed_str

    def get_balance(self):
        account = self.client.get_account()

        # Filter out balances less than 0.00003
        balances = [balance for balance in account['balances'] if float(balance['free']) > 0.00003]

        current_btc_price = self.client.get_avg_price(symbol='BTCUSDT')
        total_usd = 0

        # Go through all of the asset balances and add up their values
        for balance in balances:
            # Try to get price of asset in USDT
            try:
                price_in_usdt = self.client.get_avg_price(symbol=f"{balance['asset']}USDT")['price']
            except:
                # Attempt again to get price in BTC instead, and convert to USDT
                try:
                    price_in_btc = self.client.get_avg_price(symbol=f"{balance['asset']}BTC")['price']
                    price_in_usdt = price_in_btc * current_btc_price
                except:
                    price_in_usdt = 0
            total_usd += float(price_in_usdt) * float(balance['free'])

        return round(total_usd, 2)
