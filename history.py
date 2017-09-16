import time
import json
import logging
from text.japanese_token import JapaneseToken as Word


class History(object):
    """An history of all the words encountered.

    # Arguments
        path: The path to the file where the history is saved.
        separation_text: The text by which each entry will be
                         separated in the history file.
    """

    def __init__(self, path):
        # TODO: add backup func: store num words at init
        # save makura_bu_epoch.hist in _save if cur - init > thresh
        # TODO: add time info
        self.logger = logging.getLogger(__name__)
        self.logger.info("Creating history instance at %s." % path)
        self.path = path
        self.words = []

    def get_word(self, text):
        """Gets a word from the history.

        # Arguments
            text: The word string.

        # Returns
            A word instance if the word is present in the history,
            none otherwise.
        """
        for word in self.words:
            if word.base == text:
                return word
        return None

    def add_page(self, tokens):
        """Filters the tokens from a page and saves those
        that are words to the history file as well as
        the time they were added.

        # Arguments
            tokens: All tokens in the page.
        """
        self.logger.info("Adding page to history (%s tokens)." % len(tokens))
        tokens_added = []
        for token in tokens:
            if len(token.raw) == 0 or token.is_single_letter():
                continue
            self.add_word(token)
            tokens_added.append(token)
        return tokens_added

    def add_word(self, word):
        """Saves a new word to the history file 
        as well as the time it was added.

        # Arguments
            word: A word instance.
        """
        stored_word = self.get_word(word.base)
        if stored_word:
            self.logger.info("Merging word: %s." % word.base)
            for c in word.contexts:
                stored_word.add_context(c)
                stored_word.appearances += 1
        else:
            self.logger.info("Adding word: %s." % word.__dict__)
            self.words.append(word)
            word.appearances += 1

    def load(self):
        """Loads the history from the history file."""
        self.logger.info("Loading history.")
        with open(self.path, "r", encoding="utf8") as f:
            data = json.load(f)
        self.words = [Word(**d) for d in data]
        self.logger.info("Loaded %s words." % len(self.words))

    def save(self):
        """Saves the history to the history file."""
        with open(self.path, "w", encoding="utf8") as f:
            word_data = [word.__dict__ for word in self.words]
            json.dump(word_data, f, ensure_ascii=False, indent=4)

    def to_csv(self, path):
        self.logger.info("Exporting to CSV.")
        data = []
        for word in self.words:
            word_data = [word.base,
                         word.base_furigana,
                         word.translation,
                         ",".join(word.contexts)]
            data.append("\t".join(word_data))
        with open(path, "w", encoding="utf8") as f:
            f.write("\n".join(data))
