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
from modules.libs.td import client

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self):
        self.name = "tdameritrade"
        self.api_url = "https://api.tdameritrade.com/v1/"
        self.menu_name = "📟 TD Ameritrade"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]
        self.session = self.get_TD_session()

    def get_TD_session(self):
        TDSession = client.TDClient(
            account_number = td_ameritrade['account_number'],
            account_password = td_ameritrade['account_password'],
            consumer_id = td_ameritrade['consumer_id'],
            redirect_uri = td_ameritrade['redirect_uri']
        )
        if TDSession is not None:
            return TDSession
        else:
            raise Exception("Failed to get TDSession")

    def get_balance(self):
        accounts = self.session.get_accounts()
        total_balance = accounts[0]['securitiesAccount']['currentBalances']['liquidationValue']
        return total_balance

    def get_balance_detailed(self):
        accounts = self.session.get_accounts(fields=['positions'])
        positions = accounts[0]['securitiesAccount']['positions']
        positions_str = "----------------------\n"
        total_market_value = 0
        total_day_profitloss = 0

        for pos in positions:
            amount = round(pos['longQuantity'], 1)
            avg_purchase_price = pos['averagePrice']
            symbol = pos['instrument']['symbol']
            market_value = pos['marketValue']
            total_market_value += market_value
            currerentDayProfitLoss = pos['currentDayProfitLoss']
            total_day_profitloss += currerentDayProfitLoss
            todays_preformance = round(pos['currentDayProfitLossPercentage'], 3)
            percent_change_since_purchase = round(((market_value / (avg_purchase_price * amount)) - 1) * 100, 2)
            positions_str += f"💰 {symbol} | {amount} | ${market_value}{'📈' if todays_preformance > 0 else '📉'}${currerentDayProfitLoss}[ 24hr ]) | {todays_preformance}%[ 24hr ] | {'👍' if percent_change_since_purchase > 0 else '😱'}{percent_change_since_purchase}%[ ALL ]\n"
            positions_str += "---------------------------------------\n"
        positions_str += "---------------------------------------\n"
        positions_str += f"Total {self.menu_name} Holdings: ${total_market_value} {'👍' if total_day_profitloss > 0 else '👎'} ${round(total_day_profitloss, 2)}[ 24hr ]\n"
        positions_str += "---------------------------------------\n"
        return positions_str


