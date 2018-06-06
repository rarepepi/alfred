import config
from binance.client import Client
client = Client(config.APIKEY, config.APISECRET)


def main():
    info = client.get_account()
    print(info)


if __name__ == '__main__':
    main()
