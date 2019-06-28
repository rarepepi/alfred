from core import Alfred


def main():
    al = Alfred()
    al.run()


def test_module():
    from modules.gemini.core import Module
    client = Module(config.telegram['chat_id'])
    balance = client.balance()
    print(balance)


if __name__ == '__main__':
    testing_modules = False
    if testing_modules:
        test_module()
    else:
        main()
