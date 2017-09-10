from abc import ABC, abstractmethod


class Token(ABC):

    def __init__(self, raw, base):
        self.raw = raw
        self.base = base

    @abstractmethod
    def is_punctuation(self):
        pass

    @abstractmethod
    def is_single_letter(self):
        pass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
