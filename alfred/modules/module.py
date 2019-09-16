from abc import ABCMeta, abstractmethod
import config
import logging
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class AlfredModule(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_balance(self): pass

    @staticmethod
    def check_auth(self, msg):
        if (
            msg is not None
            and str(msg.chat_id) == config.telegram['chat_id']
            and str(msg.chat.username) == config.telegram['username']
        ):
            logger.info(f"User: {msg.chat.username}, authenticated")
            logger.info(msg.text)
            return True

        logger.info(f"User: {msg.chat.username}, failed auth")
        return False

    @staticmethod
    def get_menu_keyboard(self):
        keyboard = []
        for command in self.commands:
            command_name = command[0]
            command_func = command[1]
            keyboard.append(
                [InlineKeyboardButton(
                    f"{command_name}",
                    callback_data=f'{self.name}-{command_func}')]
                )
        keyboard.append(
            [InlineKeyboardButton('🔙 main menu', callback_data='core-main')])

        return InlineKeyboardMarkup(keyboard)
