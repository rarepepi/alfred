from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import utils
import telegram
import logging
import config
import gemini

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
commands = ['start', 'echo', 'gemini']


# Telegram commands
def start(bot, update):
    update.message.reply_text(
        "Commands are the following: ", commands)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def gemini_balance(bot, update):
    update.message.reply_text(gemini.get_balance())


def gemini_price(bot, update, args):
    symbol = "".join(args)
    symbol = "btcusd"
    update.message.reply_text(gemini.get_price(symbol))


# def gemini_commands(bot, update):
#     custom_keys = [['/balance'], ['/price']]
#     replay_markup = telegram.ReplyKeyboardMarkup(custom_keys)
#     bot.send_message(
#         text="Customer Keyboard Test",
#         chat_id=update.message.chat_id,
#         reply_markup=replay_markup)

def main_menu(bot, update):
    button_list = [
        telegram.InlineKeyboardButton("Price", callback_data=gemini_price),
        telegram.InlineKeyboardButton("Balance", callback_data=gemini_balance)

    ]
    reply_markup = telegram.InlineKeyboardMarkup(
        utils.build_menu(button_list, n_cols=2))
    bot.send_message(
        text="Eyyy",
        reply_markup=reply_markup,
        chat_id=update.message.chat_id)
    


def main():
    updater = Updater(config.telegram['token'])
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('echo', echo))
    # dp.add_handler(CommandHandler('balance', gemini_balance))
    # dp.add_handler(CommandHandler('price', gemini_price))
    # dp.add_handler(CommandHandler('gemini', gemini_price, pass_args=True))
    dp.add_handler(CommandHandler('gemini', main_menu))

    dp.add_error_handler(error) 
    dp.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
