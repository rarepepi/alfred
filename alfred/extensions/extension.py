from abc import ABCMeta, abstractmethod


class Extension(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_commands(self): pass

    @abstractmethod
    def get_menu(self): pass

    @abstractmethod
    def resolve_query(self, query): pass
