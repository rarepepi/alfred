from abc import ABCMeta, abstractmethod


class AlfredModule(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def resolve_query(self): pass

    @abstractmethod
    def main_menu(self): pass

    @abstractmethod
    def callback_handler(self, query): pass
