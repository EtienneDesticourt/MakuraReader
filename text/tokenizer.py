from abc import ABC, abstractmethod


class Tokenizer(ABC):
    """An object that provides tokenization functionnalities for text."""

    @abstractmethod
    def split(self, text):
        """Splits text into lexical tokens.

        # Arguments
            text: The text to split.

        # Returns
            A list of tokens containing info such as the token's raw string,
            base form, translation, etc...
        """
        pass