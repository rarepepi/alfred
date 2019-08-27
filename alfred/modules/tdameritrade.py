import logging
import time
import json
import base64
import hmac
import hashlib
import requests
from .module import AlfredModule
from .config import gemini

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class Module(AlfredModule):
    def __init__(self):
        self.name = "tdameritrade"
        self.menu_name = "📟 TD Ameritrade"
        self.commands = [
            ('💰 Balance', "get_balance_detailed"),
        ]

    def get_balance_detailed(self):
        return "yeerrrer"
