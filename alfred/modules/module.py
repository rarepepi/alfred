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

    def check_auth(self, msg):
        if str(msg.chat_id) == config.telegram['chat_id']:
            logger.info(f"User: {msg.chat.username}, authenticated")
            logger.info(f"msg: {msg}")
            return True

        return False
        logger.info(f"User: {msg.chat.username}, failed auth")
