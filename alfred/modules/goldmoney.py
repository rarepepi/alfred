import logging
import requests
from modules.module import AlfredModule
from modules.configs.config import goldmoney
from bs4 import BeautifulSoup
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# Gold money does not have an api, so for now this is a work around
class Module(AlfredModule):
    def __init__(self):
        self.name = "goldmoney"
        self.menu_name = "🥇 GoldMoney"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]

    def get_balance(self):
        # Get amound of gold and silver from the users config
        gold_holdings = float(goldmoney['gold'])
        silver_holdings = float(goldmoney['silver'])

        # Find the current gold and silver prices
        r = requests.get('https://www.apmex.com/gold-price')
        soup = BeautifulSoup(r.text, 'html.parser')
        gold_price = float(soup.findAll("span", {"class": "current"})[0].text.replace('$', '').replace(',', ''))
        silver_price = float(soup.findAll("span", {"class": "current"})[1].text.replace('$', '').replace(',', ''))

        # Return value of profile by multiplying amounts by price
        total_usd_value = ((gold_holdings * gold_price) + (silver_holdings * silver_price))
        return total_usd_value

    def get_balance_detailed(self):
        # Get amound of gold and silver from the users config
        gold_holdings = float(goldmoney['gold'])
        silver_holdings = float(goldmoney['silver'])

        # Find the current gold and silver prices
        r = requests.get('https://www.apmex.com/gold-price')
        soup = BeautifulSoup(r.text, 'html.parser')
        gold_price = float(soup.findAll("span", {"class": "current"})[0].text.replace('$', '').replace(',', ''))
        silver_price = float(soup.findAll("span", {"class": "current"})[1].text.replace('$', '').replace(',', ''))

        # Return value of profile by multiplying amounts by price
        total_usd_value = ((gold_holdings * gold_price) + (silver_holdings * silver_price))
        
        balance_detail_str = "------------------------------------------------------\n"
        balance_detail_str += f"🥇 Gold | {gold_holdings}oz | ${round((gold_holdings * gold_price), 2)}\n"
        balance_detail_str += f"🥈 Silver | {silver_holdings}oz | ${round((silver_holdings * silver_price), 2)}\n"
        balance_detail_str += "------------------------------------------------------\n"
        balance_detail_str += f"Total {self.menu_name} Holdings: ${round(total_usd_value, 2)}\n"
        balance_detail_str += "------------------------------------------------------\n"
        return balance_detail_str
