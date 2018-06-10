from config import CONFIG
from binance.client import Client
client = Client(CONFIG['APIKEY'], CONFIG['APISECRET'])


def main():
    info = client.get_account()
    assets = info['balances']
    for asset in assets:
        print(asset['asset'])
        print(asset['free'])


if __name__ == '__main__':
    main()
