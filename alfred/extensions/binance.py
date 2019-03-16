from extension import Extension


class Binance(Extension):
        def __init__(self):
                pass

        def get_menu():
                pass

        def get_commands():
                pass

        def resolve_query():
                pass

        # def buy_btc(self):
        #         order = self.client.create_test_order(
        #                 symbol='BNCBTC',
        #                 side=self.client.SIDE_BUY,
        #                 type=Client.ORDER_TYPE_MARKET,
        #                 quantity=quantity
        #         )

        # def get_balance():
        #         balances = []
        #         info = self.client.get_account()
        #         assets = info['balances']
        #         for asset in assets:
        #                 if float(asset['free']) > 0.001:
        #                         balances.append(
        #                                 asset['asset'],
        #                                 asset['free']
        #                         )
