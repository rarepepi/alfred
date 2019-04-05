import core
import utils

import logging
import os
import sys
from threading import Thread
import telegram
from telegram.ext import (
    CommandHandler,
    Updater,
    CallbackQueryHandler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


# Initial menu for bot start
def start(bot, update):
    keyboard = []
    for module in core.modules:
        keyboard.append(
            telegram.KeyboardButton(
                "/{}".format(module)
            )
        )
    reply_markup = telegram.ReplyKeyboardMarkup(
        utils.build_menu(
            keyboard,
            n_cols=len(keyboard)
        )
    )
    bot.send_message(
        text="Welcome!",
        chat_id=update.message.chat_id,
        reply_markup=reply_markup
    )


# Error reporting
def error(bot, update, error):
    logger.warning(
        'Update "%s" caused error "%s"',
        update,
        error
    )


def gemini_menu(bot, update):
    button_list = [
        telegram.InlineKeyboardButton(
            "BTC price",
            callback_data="gemini_btc_price"
        ),
        telegram.InlineKeyboardButton(
            "BTC balance",
            callback_data="gemini_btc_balance"
        )
    ]
    reply_markup = telegram.InlineKeyboardMarkup(
        utils.build_menu(
            button_list,
            n_cols=len(button_list)
        )
    )
    bot.send_message(
        text="Options...",
        chat_id=update.message.chat_id,
        reply_markup=reply_markup
    )


def binance_menu(bot, update):
    button_list = [
        telegram.InlineKeyboardButton(
            "Total Balances",
            callback_data="binance_total_balances"
        )
    ]
    reply_markup = telegram.InlineKeyboardMarkup(
        utils.build_menu(
            button_list,
            n_cols=len(button_list)
        )
    )
    bot.send_message(
        text="Options...",
        chat_id=update.message.chat_id,
        reply_markup=reply_markup
    )


def callback_handler(bot, update):
    query = update.callback_query.data
    text = core.get_response(query)
    bot.send_message(
        text=text,
        chat_id=update.callback_query.message.chat.id
    )


def get_menu(module):
    if module == "gemini":
        return gemini_menu
    elif module == "binance":
        return binance_menu


def is_active(extension):
    if extension[1] == "active":
        return True
    else:
        return False


def integrate_extensions():
    for extension in config.extensions:
        if is_active(extension):
            pass


def main():
    updater = Updater(config.telegram['token'])
    dp = updater.dispatcher

    def stop_and_restart():
        updater.stop()
        os.execl(
            sys.executable,
            sys.executable,
            * sys.argv
        )

    def restart(bot, update):
        update.message.reply_text('🖥 restarting system...')
        Thread(target=stop_and_restart).start()
        update.message.reply_text('🖥 system back online!')

    def add_module_handlers():
        for module in core.modules:
            dp.add_handler(
                CommandHandler(
                    module,
                    get_menu(module)
                )
            )

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('r', restart))
    dp.add_handler(CallbackQueryHandler(callback_handler))
    dp.add_error_handler(error)

    add_module_handlers()

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
