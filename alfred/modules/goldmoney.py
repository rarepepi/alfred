import logging
import requests
from modules.module import AlfredModule
from modules.configs.config import goldmoney

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self):
        self.name = "goldmoney"
        self.menu_name = "🥇 GoldMoney"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]
        self.api_url = "https://wealth-api.goldmoney.com/"

    def request(self, method, path, payload=None):
        request_method = requests.Session().get if method == 'get' else requests.Session().post
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "cookie": parser.get('GoldMoney', 'cookie')
        }

        r = request_method(self.api_url + path, data=payload, headers=headers)
        if r.status_code == 200:
            logger.info(r.text)
            logger.info(f"Request headers:\n {r.headers}")
            self.save_new_cookie(r)
            json = r.json()
            return json
        else:
            logger.error("Failed")

    def save_new_cookie(self, r):
        request_cookies = r.cookies.items()
        new_cookie_str = f"__cfduid={request_cookies[0]}; gmsid={request_cookies[1]}; goldmoney_payload={request_cookies[2]}; PLAY_LANG=en-US"

        parser.set('GoldMoney', 'cookie', new_cookie_str)
        fp = open(f'{dir_path}/config.ini', 'w')
        parser.write(fp)
        fp.close()


    def get_balance(self):
        # self.login()
        # r = self.request('get', 'balances')
        # metals = r['metals']
        # fiat_usd = r['fiat'][0]['balance']['amount']
        # total_usd = fiat_usd

        # for metal in metals:
        #     if metal['currencyCode'] == 'Gold':
        #         total_usd += metal['equivalent']['amount']
        #     if metal['currencyCode'] == 'Silver':
        #         total_usd += metal['equivalent']['amount']
        # return total_usd
        return 1945

    def get_balance_detailed(self):
        self.login()
        r = self.request('get', 'balances')
        balance_detail_str = "------------------------------------------------------\n"
        metals = r['metals']
        fiat_usd = r['fiat'][0]['balance']['amount']
        balance_detail_str += f"💵 Cash | ${fiat_usd}\n"
        total_usd = fiat_usd

        total_gold_onces = 0
        total_silver_onces = 0
        total_gold_usd = 0
        total_silver_usd = 0
        unit = ""
        for metal in metals:
            if metal['currencyCode'] == 'Gold':
                total_gold_onces += metal['balance']['amount']
                total_usd += metal['equivalent']['amount']
                total_gold_usd += metal['equivalent']['amount']
                unit = "g"
            if metal['currencyCode'] == 'Silver':
                total_silver_onces += metal['balance']['amount']
                total_usd += metal['equivalent']['amount']
                total_silver_usd += metal['equivalent']['amount']
                unit = "oz"

            balance_detail_str += f"💰 {metal['currencyCode']} | {metal['balance']['amount']}{unit} | ${metal['equivalent']['amount']} | {metal['vault']}\n"
        balance_detail_str += "------------------------------------------------------\n"
        balance_detail_str += f"Total {self.menu_name} Holdings: ${total_usd}\n"
        balance_detail_str += "------------------------------------------------------\n"
        return balance_detail_str
