import importlib
import config

extension_name = 0
extension_status = 1
objects = []

for extension in config.extensions:
    if extension[extension_status] == "active":
        print(extension[extension_name])
        objects.append(importlib.import_module(extension[extension_name]))

for obj in objects:
    print(object)


def get_response(query):
    if query == "gemini_btc_price":
        return extensions.Gemini.get_btc_price()

    elif query == "gemini_btc_balance":
        return extensions.Gemini.get_btc_balance()

    elif query == "binance_total_balances":
        return extensions.Binance.get_balance()

    elif query == "goldmoney_total_balances":
        return extensions.Goldmoney.get_balance()
