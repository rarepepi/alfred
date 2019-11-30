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
        self.updater = Updater(
            config.telegram['token'],
            use_context=True
        )
        self.dp = self.updater.dispatcher
        self.chat_id = config.telegram['chat_id']
        self.module_commands = []
        self.main_commands = [
            ('💾 Exchanges 💾', 'modules'),
            ('💯 Portfolio 💯', 'portfolio'),
            ('💸 Total Balance 💸', 'total_balance')

        ]

        # Imports the modules that are marked as active in the config
        self.active_modules = self.import_active_modules(config.modules)

        # Adds the default handlers used for basic commands/menu
        self.add_core_callback_handlers()

        # Adds the handlers for the modules and their respective menus
        self.get_active_modules_commands()

    # Sends the main menu upon the /yo command
    def start(self, update, context):
        msg = update.message
        if self.check_auth(msg):
            msg.reply_text(
                "Main Menu Commands",
                reply_markup=self.get_main_menu_keyboard()
            )

    # Main menu response to back button
    def main_menu(self, update, context):
        query = update.callback_query
        bot = context.bot
        if self.check_auth(query.message):
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Main Menu Commands",
                reply_markup=self.get_main_menu_keyboard())

    def modules_menu(self, update, context):
        query = update.callback_query
        bot = context.bot
        if self.check_auth(query.message):
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text="Modules",
                reply_markup=self.get_modules_keyboard())

    def callback_handler(self, update, context):
        msg = update.callback_query.message
        query = update.callback_query.data
        bot = context.bot
        if self.check_auth(msg):
            try:
                logger.info(f"Got msg: {query}")
                mod_name = query[:query.find('-')]
                if "core-" in query:
                    core_command = query[query.find('-')+1:]
                    core_func = getattr(self, core_command)
                    text = core_func()
                    bot.send_message(
                        text=text,
                        chat_id=update.callback_query.message.chat.id
                    )
                elif mod_name in [mod.name for mod in self.active_modules]:
                    logger.info(f"Got command for {mod_name} ...")
                    mod_command = query[query.find('-')+1:]
                    mod = next((x for x in self.active_modules if x.name == mod_name))
                    if "-main" in query:
                        mod_func = getattr(mod, "get_menu_keyboard")
                        keyboard = mod_func(mod)
                        bot.edit_message_text(
                            chat_id=msg.chat_id,
                            message_id=msg.message_id,
                            text="Modules",
                            reply_markup=keyboard)
                        return
                    mod_func = getattr(mod, mod_command)
                    text = mod_func()
                    bot.send_message(
                        text=text,
                        chat_id=update.callback_query.message.chat.id
                    )
            except StopIteration:
                logger.error(f"{query} is not a command")

    def restart(self, update, context):
        # OUT OF SERVICE
        if self.check_auth(update.message):
            self.updater.stop()
            os.execl(
                sys.executable,
                sys.executable,
                * sys.argv
            )
            update.message.reply_text('🖥 restarting system...')
            update.message.reply_text('🖥 system back online!')

    def error(self, update, context, error):
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
                logger.info(f"trying to import {mod_name}...")
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

    def get_active_modules_commands(self):
        for mod in self.active_modules:
            logger.info(f"Adding commands for {mod.name} module")
            self.module_commands.append(mod.commands)

    def get_main_menu_keyboard(self):
        keyboard = []
        for cmd in self.main_commands:
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


    def total_balance(self):
        total = 0
        # Go into every running module
        for mod in self.active_modules:
            total += mod.get_balance()
        return round(total, 2)

    def portfolio(self):
        assets = config.portfolio['assets']
        porfolio_str = "Portfolio Splits\n"
        porfolio_str += "--------------------------\n"
        for a in assets:
            porfolio_str += f"{a['class']} | {a['allocation']}\n"
        return porfolio_str


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
