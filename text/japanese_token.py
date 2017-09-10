from text.token import Token


class JapaneseToken(Token):

    def __init__(self, raw, base, furigana, translation, contexts):
        super().__init__(raw, base)
        self.furigana = furigana
        self.translation = translation
        self.contexts = contexts

    def is_punctuation(self):
        return False

    def is_single_letter(self):
        return False

    def has_kanji(self):
        return False

    def strip(self):
        pass

    def add_context(self, context):
        if context not in self.contexts:
            self.contexts.append(context)
