
from extension import Extension
import requests
import config


class Goldmoney(Extension):
        def get_menu():
            pass

        def get_commands():
            pass

        def resolve_query():
            pass

        def get_balance():
            payload = {
                "name": config.goldmoney['holding'],
                "password": config.goldmoney['password']
            }
            r = requests.post(
                'https://holding.goldmoney.com/overview/balances',
                data=payload
            )
