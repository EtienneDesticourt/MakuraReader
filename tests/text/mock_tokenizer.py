import text.tokenizer
from text.japanese_token import JapaneseToken


class MockTokenizer(text.tokenizer.Tokenizer):
    """A mock tokenizer to be used in tests where a text needs to be split into tokens."""

    def split(self, text):
        tokens = []
        for i in range(10):
            token = JapaneseToken("戻りました%s" % i, "戻ります%s" % i,
                                  "もどります%s" % i, "to return %s" % i,
                                  ["急いで羽田空港に戻りました。%s" % i])
            tokens.append(token)

        return tokens
