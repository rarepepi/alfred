from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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
        "Commands are the following: %s", commands)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def gemini_balance(bot, update):
    update.message.reply_text(gemini.get_balance())

def main():
    updater = Updater(config.telegram['token'])
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('echo', echo))
    dp.add_handler(CommandHandler('balance', gemini_balance()))

    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
