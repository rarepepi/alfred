import config
import utils
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
        self.updater = Updater(config.telegram['token'])
        self.dp = self.updater.dispatcher
        self.chat_id = config.telegram['chat_id']
        self.commands = [
            ('💾 Modules 💾', 'modules'),
            ('💸 Net Worth 💸', 'net', self.net_worth)
        ]

        # Imports the modules that are marked as active in the config
        self.active_modules = self.import_active_modules(config.modules)

        # Adds the default handlers used for basic commands/menu
        self.add_core_callback_handlers()

        # Adds the handlers for the modules and their respective menus
        self.add_active_module_handlers()

    # Sends the main menu upon the /yo command
    def start(self, bot, update):
        msg = update.message
        if self.check_auth(msg):
            msg.reply_text(
                "Main Menu Commands",
                reply_markup=self.get_main_menu_keyboard()
            )

    # Main menu response to back button
    def main_menu(self, bot, update):
        query = update.callback_query
        if self.check_auth(query.message):
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Main Menu Commands",
                reply_markup=self.get_main_menu_keyboard())

    def modules_menu(self, bot, update):
        query = update.callback_query
        if self.check_auth(query.message):
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text=f"Modules",
                reply_markup=self.get_modules_keyboard())

    def callback_handler(self, bot, update):
        query = update.callback_query
        if self.check_auth(update.message):
            try:
                command = query.data
                logger.info(f"Recieved query: {command}")
                if 'core' in command:
                    logger.info(f"Got command: {command}")
                    func = next(
                        cmd for cmd in self.commands if f"core-{cmd[1]}" == command)[2]
                    text = func()
                    bot.send_message(
                        text=text,
                        chat_id=update.callback_query.message.chat.id
                    )
            except StopIteration:
                logger.error(f"{query} is not a command")

    def restart(self, bot, update):
        if self.check_auth(update.message):
            self.updater.stop()
            os.execl(
                sys.executable,
                sys.executable,
                * sys.argv
            )
            update.message.reply_text('🖥 restarting system...')
            Thread(target=self.stop_and_restart).start()
            update.message.reply_text('🖥 system back online!')

    def error(self, bot, update, error):
        logger.warning(
            'Update "%s" caused error "%s"',
            update,
            error
        )

    def wake_up(self):
        logging.info("Starting bot polling ...")
        self.updater.start_polling()
        self.updater.idle()

    # Used to check if a the message matches the chat_id in Alfred
    def check_auth(self, msg):
        if (
            msg is not None
            and str(msg.chat_id) == config.telegram['chat_id']
            and str(msg.chat.username) == config.telegram['username']
        ):
            logger.info(f"User: {msg.chat.username}, authenticated")
            return True

        return False
        logger.info(f"User: {msg.chat.username}, failed auth")

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

                logger.info(f"Attemping to import {mod_name}...")
                module = importlib.import_module(
                    f'.{mod_name}', 'modules')
                active_and_imported.append(module.Module())
                logger.info(f"{mod_name} module imported")
            except Exception as e:
                logger.error(f"could not import extension: {e}")
        return active_and_imported

    def add_core_callback_handlers(self):
        logger.info("Adding core handlers ...")
        self.dp.add_handler(CommandHandler('yo', self.start))
        self.dp.add_handler(CommandHandler('restart', self.restart))
        self.dp.add_handler(CallbackQueryHandler(
            self.main_menu, pattern='core-main'))
        self.dp.add_handler(CallbackQueryHandler(
            self.modules_menu, pattern='core-modules'))
        self.dp.add_handler(CallbackQueryHandler(
            self.callback_handler))
        self.dp.add_error_handler(self.error)

    def add_active_module_handlers(self):
        for mod in self.active_modules:
            logger.info(f"Adding menu handlers for {mod.name} module")
            self.dp.add_handler(CallbackQueryHandler(mod.main_menu, pattern=f'{mod.name}-main'))
            # self.dp.add_handler(CallbackQueryHandler(mod.callback_handler))

    def get_main_menu_keyboard(self):
        keyboard = []
        for cmd in self.commands:
            keyboard.append(
                [InlineKeyboardButton(
                    f"{cmd[0]}",
                    callback_data=f"core-{cmd[1]}")]
            )
        return InlineKeyboardMarkup(keyboard)

    def get_modules_keyboard(self):
        keyboard = []
        for mod in self.active_modules:
            keyboard.append(
                [InlineKeyboardButton(
                    f"{mod.menu_name}",
                    callback_data=f'{mod.name}-main')]
            )
        keyboard.append(
            [InlineKeyboardButton('🔙 main menu', callback_data='core-main')])

        return InlineKeyboardMarkup(keyboard)

    def get_total_balance(self):
        for mod in self.active_modules:
            total += mod.get_balance()

    def net_worth(self):
        return 100


def main():
    logger.info("Starting Alfred server ...")
    al = Alfred()
    al.wake_up()


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
