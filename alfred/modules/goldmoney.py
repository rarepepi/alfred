import logging
import requests
from .module import AlfredModule
from .config import goldmoney
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self):
        self.name = "goldmoney"
        self.menu_name = "🥇 GoldMoney"
        self.commands = [
            ('balance', self.get_balance),
        ]

        def main_menu(self, bot, update):
            logger.info("Goldmoney main menu called")
            keyboard = []
            for command in self.commands:
                command_name = command[0]
                keyboard.append(
                    [InlineKeyboardButton(
                        f"{command_name}",
                        callback_data=f'{self.name}-{command_name}')]
                    )
            keyboard.append(
                [InlineKeyboardButton('🔙 main menu', callback_data='core-main')])
    
            query = update.callback_query
            if self.check_auth(query.message):
                bot.edit_message_text(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text="Goldmoney Main Menu",
                    reply_markup=InlineKeyboardMarkup(keyboard))
    
        def callback_handler(self, bot, update):
            msg = update.callback_query.message
            if self.check_auth(msg):
                try:
                    command = update.callback_query.data
                    func = next(
                        cmd for cmd in self.commands if f"{self.name}-{cmd[0]}" == command)[1]
                    text = func()
                    bot.send_message(
                        text=text,
                        chat_id=update.callback_query.message.chat.id
                    )
                except StopIteration:
                    logger.error(f"{msg} is not a command")
    
    def get_balance(self):
        headers = {
            'cookie': goldmoney['cookie']
        }
        return "gm balance"
