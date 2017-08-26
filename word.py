

class Word(object):
    """A word of vocabulary. Holds related information such as
    translation, furigana and context.

    # Arguments
        word: The word in question.
        furigana: The hiragana transcription of the word.
        translation: The english translation of the word.
        definition: The definition of the word in english.
        context: A list of sentences in which the word appeared.
    """

    def __init__(self, word, furigana, translation, definition, contexts):
        self.word = word
        self.furigana = furigana
        self.translation = translation
        self.definition = definition
        self.contexts = contexts

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
