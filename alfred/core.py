from . import config, utils
import logging
import importlib
import os
import sys
from threading import Thread
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    CommandHandler,
    Updater,
    CallbackQueryHandler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Alfred(object):
    def __init__(self):
        # Set the updater server/polling with api token
        self.updater = Updater(config.telegram['token'])

        # Get dispatcher for messages
        self.dp = self.updater.dispatcher

        # Use the chat id to identify if the bot is in the proper chat room
        self.chat_id = config.telegram['chat_id']

        # Imports all of the modules that are marked as being active
        self.active_modules = self.import_active_modules(config.modules)

        # Adds the default handlers used for basic commands/menu
        self.add_default_handlers()
        
        # Adds the handlers for the modules and their respective menus
        self.add_active_module_handlers()

    # Used to check if a the message matches the chat_id in Alfred
    def check_auth(self, message):
        if str(message.chat_id) == self.chat_id:
            logger.info(f"User: {message.chat.username}, authenticated")
            return True
        return False

    # Attempts to import all active modules
    def import_active_modules(self, modules):
        logger.info("Importing active modules ...")
        # Creates a list of the all the modules which a true value in active
        active = [mod for mod in modules if mod['active']]

        # Goes through the module 
        active_and_imported = []
        for mod in active:
            try:
                mod_name = mod['name'].lower()
                module = importlib.import_module(
                    f'modules.{mod_name}.core', '.')
                active_and_imported.append(module.Module(self.chat_id))
                logger.info(f"{mod_name} module imported")
            except Exception as e:
                logger.error(f"could not import extension: {e}")
        return active_and_imported

    def add_default_handlers(self):
        logger.info("Adding default handlers ...")
        self.dp.add_handler(
            CommandHandler('start', self.start))
        self.dp.add_handler(
            CallbackQueryHandler(self.main_menu, pattern='core-main'))
        self.dp.add_handler(
            CommandHandler('restart', self.restart))

        self.dp.add_error_handler(self.error)

    def add_active_module_handlers(self):
        for module in self.active_modules:
            logger.info(f"Adding menu handlers for {module.name} module")
            self.dp.add_handler(
                CallbackQueryHandler(
                    module.main_menu, pattern=f'{module.name}-main'))
            self.dp.add_handler(
                CallbackQueryHandler(
                    module.callback_handler))

    def main_menu(self, bot, update):
        query = update.callback_query
        message = update.message
        if message is None:
            message = query.message
        if self.check_auth(message):
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Main Commands",
                reply_markup=self.main_menu_keyboard())

    def main_menu_keyboard(self):
        keyboard = utils.get_menus_of_active_modules()
        return InlineKeyboardMarkup(keyboard)

    def start(self, bot, update):
        if self.check_auth(update.message):
            update.message.reply_text(
                "Modules",
                reply_markup=self.main_menu_keyboard())

    def stop_and_restart(self):
        self.updater.stop()
        os.execl(
            sys.executable,
            sys.executable,
            * sys.argv
        )

    def restart(self, bot, update):
        if self.check_auth(update.message):
            update.message.reply_text('🖥 restarting system...')
            Thread(target=self.stop_and_restart).start()
            update.message.reply_text('🖥 system back online!')

    def error(self, bot, update, error):
        logger.warning(
            'Update "%s" caused error "%s"',
            update,
            error
        )

    def run(self):
        logging.info("Starting bot polling")
        self.updater.start_polling()
        self.updater.idle()


def main():
    al = Alfred()
    al.run()


def test_module():
    from modules.gemini import Module
    client = Module(config.telegram['chat_id'])
    balance = client.balance()
    print(balance)


if __name__ == '__main__':
    testing_modules = False
    if testing_modules:
        test_module()
    else:
        main()
