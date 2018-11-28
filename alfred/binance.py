from binance.client import Client


class Binance():
    """
    A Binance plugin for the Alfred
    plugin system
    """

    def __init__(self, apiKey, apiSecret):
        self.key = apiKey
        self.secret = apiSecret
        self.client = Client(self.key, self.secret)

    def buy_btc(self, quantity, price):
        order = self.client.create_test_order(
            symbol='BNCBTC',
            side=self.client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity)

    def get_balance(self):
        balances = []
        info = self.client.get_account()
        assets = info['balances']
        for asset in assets:
            if float(asset['free']) > 0.001:
                balances.append((asset['asset'], asset['free']))

        return balances
