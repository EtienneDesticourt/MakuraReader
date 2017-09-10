import time
import json
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

    def add_word(self, word):
        """Saves a new word to the history file 
        as well as the time it was added.

        # Arguments
            word: A word instance.
        """
        stored_word = self.get_word(word.base)
        if stored_word:
            for c in word.contexts:
                stored_word.add_context(c)
        else:
            self.words.append(word)
        self.save()

    def load(self):
        """Loads the history from the history file."""
        with open(self.path, "r", encoding="utf8") as f:
            data = json.load(f)
        self.words = [Word(**d) for d in data]

    def save(self):
        """Saves the history to the history file."""
        with open(self.path, "w", encoding="utf8") as f:
            word_data = [word.__dict__ for word in self.words]
            json.dump(word_data, f, ensure_ascii=False, indent=4)

    def to_csv(self, path):
        data = []
        for word in self.words:
            word_data = [word.base,
                         word.furigana,
                         word.translation,
                         ",".join(word.contexts)]
            data.append("\t".join(word_data))
        with open(path, "w", encoding="utf8") as f:
            f.write("\n".join(data))
