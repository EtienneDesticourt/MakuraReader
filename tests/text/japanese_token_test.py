"""Various tests for japanese tokens.
These tests don't test the full set of possibilities but should be
enough to be fairly confident that the tokens do what they're supposed
to. """
from text.japanese_token import JapaneseToken

TEST_TOKEN = JapaneseToken("戻りました", "戻ります",
                           "もどりました", "もどります",
                           "to return ",
                           ["急いで羽田空港に戻りました。"])


def test_is_punctuation():
    point = JapaneseToken("。", "。", "。", "。", ".",
                          ["急いで羽田空港に戻りました。"])
    assert point.is_punctuation()
    assert TEST_TOKEN.is_punctuation() == False


def test_is_single_letter():
    single = JapaneseToken("い", "い", "い", "い", "い",
                           ["急いで羽田空港に戻りました。"])
    assert single.is_single_letter()
    assert TEST_TOKEN.is_single_letter() == False


def test_is_kanji():
    assert TEST_TOKEN.is_kanji("羽")
    assert TEST_TOKEN.is_kanji("で") == False
    assert TEST_TOKEN.is_kanji("a") == False
    assert TEST_TOKEN.is_kanji("。") == False


def test_has_kanji():
    no_kanji = JapaneseToken("もどりました", "もどります",
                             "もどりました", "もどります",
                             "to return ",
                             ["急いで羽田空港にもどりました。"])
    assert no_kanji.has_kanji() == False
    assert TEST_TOKEN.has_kanji()


def test_strip():
    result = TEST_TOKEN.strip()
    assert len(result) == 3
    kanji_head, furi_head, tail = result
    assert kanji_head == "戻"
    assert furi_head == "もど"
    assert tail == "りました"
