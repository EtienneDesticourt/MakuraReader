from history import History
from word import Word
from tests.config import history_config


def test_add_get_word_first_time():
    hist = History(**history_config)
    word1 = Word("人間", "にんげん", "human",
                 ["その子、人間じゃないの。ロボットなのよ。アンドロイド。"])
    word2 = Word("愛", "あい", "love",
                 ["君が私を愛している以上に私は君を愛している。"])
    hist.add_word(word1)
    hist.add_word(word2)

    should_be_word2 = hist.get_word("愛")
    should_be_word1 = hist.get_word("人間")
    assert should_be_word2 and should_be_word2 == word2
    assert should_be_word1 and should_be_word1 == word1


def test_add_get_word_already_stored_different_context():
    hist = History(**history_config)
    context1 = "その子、人間じゃないの。ロボットなのよ。アンドロイド。"
    context2 = "人間、そっくりね。ロボットの手まで、暖いわよ。"
    word1 = Word("人間", "にんげん", "human", [context1])
    word2 = Word("人間", "にんげん", "human", [context2])
    hist.add_word(word1)
    hist.add_word(word2)

    stored = hist.get_word("人間")
    assert stored
    assert context1 in stored.contexts
    assert context2 in stored.contexts


def test_add_get_word_already_stored_same_context():
    hist = History(**history_config)
    context1 = "その子、人間じゃないの。ロボットなのよ。アンドロイド。"
    word1 = Word("人間", "にんげん", "human", [context1])
    word2 = Word("人間", "にんげん", "human", [context1])
    hist.add_word(word1)
    hist.add_word(word2)

    stored = hist.get_word("人間")
    assert stored
    assert len(stored.contexts) == 1
    assert context1 in stored.contexts


def test_save_load():
    hist = History(**history_config)
    word1 = Word("人間", "にんげん", "human",
                 ["その子、人間じゃないの。ロボットなのよ。アンドロイド。"])
    word2 = Word("愛", "あい", "love",
                 ["君が私を愛している以上に私は君を愛している。"])
    hist.add_word(word1)
    hist.add_word(word2)
    del hist

    hist2 = History(**history_config)
    hist2.load()

    should_be_word2 = hist2.get_word("愛")
    should_be_word1 = hist2.get_word("人間")
    assert should_be_word2 and should_be_word2 == word2
    assert should_be_word1 and should_be_word1 == word1
