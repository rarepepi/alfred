import logging
import os
import sys
from threading import Thread

import config
import gemini
import telegram
import utils
from telegram.ext import (
    CommandHandler, Updater, CallbackQueryHandler)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


# Telegram commands
def start(bot, update):
    update.message.reply_text(
        "Hello and welcome!: ")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def gemini_menu(bot, update):
    button_list = [
        telegram.InlineKeyboardButton(
            "BTC price", callback_data="gemini_btc_price"),
        telegram.InlineKeyboardButton(
            "BTC balance", callback_data="gemini_btc_balance")

    ]
    reply_markup = telegram.InlineKeyboardMarkup(
        utils.build_menu(button_list, n_cols=2))
    bot.send_message(
        text="Options...",
        chat_id=update.message.chat_id,
        reply_markup=reply_markup
        )


def callback_handler(bot, update):
    query = update.callback_query.data
    if query == "gemini_btc_price":
        text = gemini.get_btc_price()
    elif query == "gemini_btc_balance":
        text = gemini.get_btc_balance()
    bot.send_message(
        text=text,
        chat_id=update.callback_query.message.chat.id
    )


def main():
    updater = Updater(config.telegram['token'])
    dp = updater.dispatcher

    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, * sys.argv)

    def restart(bot, update):
        update.message.reply_text('🖥 restarting system...')
        Thread(target=stop_and_restart).start()
        update.message.reply_text('🖥 system back online!')

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('gemini', gemini_menu))
    dp.add_handler(CommandHandler('r', restart))
    dp.add_handler(CallbackQueryHandler(callback_handler))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
