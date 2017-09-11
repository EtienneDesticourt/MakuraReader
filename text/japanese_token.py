from text.token import Token


class JapaneseToken(Token):
    """A token that may contain japanese characters.

    # Arguments
        raw: The raw form of the token as it appears in the source text.
        base: The basic, unconjugated form of the token.
        raw_furigana: The raw form with kanjis replaced by kana.
        base_furigana: The base form with kanjis replaced by kana.
        translation: The english translation of the token.
        contexts: A list of sentences the token was found in.
    """

    def __init__(self, raw, base, raw_furigana, base_furigana, translation, contexts, appearances=0):
        super().__init__(raw, base)
        self.raw_furigana = raw_furigana
        self.base_furigana = base_furigana
        self.translation = translation
        self.contexts = contexts
        # It doesn't really make sense here but I'm not
        # gonna add a whole class to store that number
        self.appearances = appearances 

    def is_punctuation(self):
        if len(self.raw) == 1:
            code = ord(self.raw)
            if code >= 0x3000 and code <= 0x303F:
                return True
        return False

    def is_single_letter(self):
        if len(self.raw) == 1 and not self.has_kanji():
            return True
        return False

    def is_kanji(self, character):
        code = ord(character)
        if (code >= 0x4E00 and code <= 0x9FAF) or (code >= 0x3400 and code <= 0x4DBF):
            return True
        return False

    def has_kanji(self):
        for character in self.raw:
            if self.is_kanji(character):
                return True
        return False

    def strip(self):
        """Strips the kana at the end of the raw token, keeping only
        the smallest part containing kanji.

        # Returns
            The raw kanji head of the token, the raw furigana for the head, the raw kana tail
        """
        for i, c in enumerate(self.raw[::-1]):
            if self.is_kanji(c):
                break
        return self.raw[:-i], self.raw_furigana[:-i], self.raw[-i:]

    def add_context(self, context):
        """Adds a sentence to the list of contexts.

        # Arguments
            context: The sentence to add.
        """
        if context not in self.contexts:
            self.contexts.append(context)
