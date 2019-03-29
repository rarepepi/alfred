# TODO extensions need names, menus, and commands
# TODO create default menues/commands like starting bot, restart, etc
# TODO utils file to help create menues, etc.
# TODO in core just check config and import all modules and create handlers/pass on api keys

# TODO also need testing/logging/error handleing
# TODO deployment
import telegram
from telegram.ext import (
    CommandHandler,
    Updater,
    CallbackQueryHandler
)
import logging
import config
import modules
from modules import default

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class Alfred(object):
    def __init__(self):
        self.updater = Updater(config.telegram['token'])
        self.dp = self.updater.dispatcher

    def add_handlers(self):
        logging.info("Adding command handlers")
        self.dp.add_handler(CommandHandler('start', default.start))

    def implement_extensions(self):
        extensions = config.extensions
        for ext in extensions:
            if extensions['enabled'] == 'True':
                print(extensions['name'])

    def start(self):
        self.add_handlers()

        logging.info("Starting bot polling")
        self.updater.start_polling()
        self.updater.idle()


def main():
    al = Alfred()
    al.start()


if __name__ == '__main__':
    main()
