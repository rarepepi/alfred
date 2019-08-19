from abc import ABCMeta, abstractmethod
import config
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class AlfredModule(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def main_menu(self): pass

    @abstractmethod
    def callback_handler(self, query): pass

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
