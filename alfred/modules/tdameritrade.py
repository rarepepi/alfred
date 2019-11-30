import logging
import json
import base64
import hmac
import hashlib
import requests
from .module import AlfredModule
from .config import td_ameritrade
import urllib.parse
import configparser
import logging
import os 

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

parser = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
parser.read(f'{dir_path}/config.ini')


class Module(AlfredModule):
    def __init__(self):
        self.name = "tdameritrade"
        self.api_url = "https://api.tdameritrade.com/v1/"
        self.menu_name = "📟 TD Ameritrade"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]

    def request(self, method, path, payload=None):
        request_method = requests.get if method == 'get' else requests.post
        headers = {
            "Authorization": f"Bearer {parser.get('TDAmeritrade', 'AccessToken')}"
        }

        r = request_method(self.api_url + path, data=payload, headers=headers)
        if r.status_code == 200:
            json = r.json()
            return json
        else:
            self.refresh_token()
            r = request_method(self.api_url + path, data=payload, headers=headers)
            json = r.json()
            return json

    def refresh_token(self):
        refresh_token = parser.get('TDAmeritrade', 'RefreshToken')
        access_token = parser.get('TDAmeritrade', 'AccessToken')

        params = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'access_type': 'offline',
            'client_id': td_ameritrade['client_id']
        }
        payload = urllib.parse.urlencode(params)
        r = self.request('post', 'oauth2/token', payload)
        parser.set('TDAmeritrade', 'AccessToken', r['access_token'])
        parser.set('TDAmeritrade', 'RefreshToken', r['refresh_token'])

        fp=open(f'{dir_path}/config.ini','w')
        parser.write(fp)
        fp.close()


    def get_balance(self):
        r = self.request('get', 'accounts')
        total_balance = r[0]['securitiesAccount']['currentBalances']['liquidationValue']
        return total_balance

    def get_balance_detailed(self):
        r = self.request('get', 'accounts?fields=positions')
        positions = r[0]['securitiesAccount']['positions']
        positions_str = "List of postitons"
        positions_str = "AMOUNT TICKER | MARKET_VALUE | 24hr_PRICE_CHANGE | PURCHASE_PRICE_CHANGE\n"
        positions_str += "-----------------------------------------------------------\n"
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
            positions_str += f"({amount}){symbol} | ${market_value}(24hr: {'📈' if todays_preformance > 0 else '📉'}{currerentDayProfitLoss}) | {todays_preformance}% | {'📈' if percent_change_since_purchase > 0 else '📉'}{percent_change_since_purchase}%\n"
        positions_str += "-----------------------------------------------------------\n"
        positions_str += f"Total Profit Loss Today: {total_day_profitloss}             Total Market Value: {total_market_value}"
        return positions_str
