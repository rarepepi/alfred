import logging
import json
import base64
import hmac
import hashlib
import requests
from modules.module import AlfredModule
from modules.configs.config import td_ameritrade

import logging
import os 
from td.client import TDClient

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self):
        self.name = "tdameritrade"
        self.api_url = "https://api.tdameritrade.com/v1/"
        self.menu_name = "📈 TD Ameritrade"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]
        self.session = self.get_TD_session()

    def get_TD_session(self):
        TDSession = TDClient(
            client_id = td_ameritrade['consumer_id'],
            redirect_uri = td_ameritrade['redirect_uri'],
            account_number = td_ameritrade['account_number'],
            credentials_path=f"{os.path.dirname(os.path.abspath(__file__))}/configs/td_keys.json"
        )
        TDSession.login()
        return TDSession

    def get_balance(self):
        accounts = self.session.get_accounts()
        total_balance = accounts[0]['securitiesAccount']['currentBalances']['liquidationValue']
        return total_balance

    def get_balance_detailed(self):
        accounts = self.session.get_accounts(fields=['positions'])
        positions = accounts[0]['securitiesAccount']['positions']
        positions_str = "---------------------------------------\n"
        total_market_value = 0
        total_day_profitloss = 0

        for pos in positions:
            amount = round(pos['longQuantity'], 1)
            avg_purchase_price = pos['averagePrice']
            symbol = pos['instrument']['symbol']
            market_value = pos['marketValue']
            total_market_value += market_value
            positions_str += f"💰 {symbol} | {amount} | ${market_value}\n"
        positions_str += "--------------------------------------------------\n"
        positions_str += f"Total {self.menu_name} Holdings: ${round(total_market_value, 2)}\n"
        positions_str += "--------------------------------------------------\n"
        return positions_str
