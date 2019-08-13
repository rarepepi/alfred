import logging
import requests
from .module import AlfredModule
from .config import gemini_keys
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
        keyboard = []
        for command in self.commands:
            command_name = command[0]
            keyboard.append(
                [InlineKeyboardButton(
                    '{}'.format(command_name),
                    callback_data=f'{self.name}-{command_name}')]
                )
        keyboard.append(
            [InlineKeyboardButton('🔙 main menu', callback_data='core-main')])

        msg = update.callback_query.message
        bot.edit_message_text(
            chat_id=msg.chat_id,
            message_id=msg.message_id,
            text=f"{self.name.title()} Commands",
            reply_markup=InlineKeyboardMarkup(keyboard))

    def callback_handler(self, bot, update):
        msg = update.callback_query.message
        if self.check_auth(msg):
            command = update.callback_query.data
            func = next(
                cmd for cmd in self.commands if f"{self.name}-{cmd[0]}" == command)[1]
            text = func()
            bot.send_message(
                text=text,
                chat_id=update.callback_query.message.chat.id
            )
    
    def get_balance(self):
        pass
