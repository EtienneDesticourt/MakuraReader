import re

class Token(object):
    "A single lexical unit."

    def __init__(self, raw, kana, stripped_kanji, stripped_kana, tail, base, english, is_kanji):
        self.raw        = raw
        self.kana       = kana
        self.stripped_kanji = stripped_kanji
        self.stripped_kana = stripped_kana 
        self.tail = tail
        self.base       = base
        self.english    = english
        self.english_first = ""
        try:
            english_results = re.findall("/\((?:n|adj|v).*?\) (?:\(.*?\))*(.*?)(?:/|\()", english[-1])

            if len(english_results) > 0:
                self.english_first = english_results[0]
        except IndexError:
            pass
        self.is_kanji   = is_kanji
