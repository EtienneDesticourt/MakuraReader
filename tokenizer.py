from collections import namedtuple
import socket
import time
from juman import juman_launcher
import utils.misc
from dic_fetcher import DicFetcher
from makura_token import Token


class TokenizerException(Exception): pass


class Tokenizer():
    JUMAN_LAUNCH_COMMAND = b"RUN -e2\n"
    JUMAN_LAUNCH_ACK = b"OK"
    JUMAN_DISCARD_CHR = "@"
    KANA_LIST = list(range(0x3000, 0x303F)) + list(range(0x3040, 0x309F)) + list(range(0x30A0, 0x30FF)) + list(range(0xFF00, 0xFFEF))

    def __init__(self):
        juman_launcher.JumanLauncher.launch()
        time.sleep(1)
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('localhost', 32000))
        except ConnectionRefusedError:
            raise TokenizerException("JUMAN server isn't running.")

        # TODO: add timeout
        self.sock.send(self.JUMAN_LAUNCH_COMMAND)
        data = b""
        while self.JUMAN_LAUNCH_ACK not in data:
            data = self.sock.recv(1024)

        self.dictionary = None

    def _query_juman(self, text):
        # TODO: add timeout     
        self.sock.sendall((text+"\n").encode("shift-jis"))
        data = b""
        while b"EOS" not in data:
            recv = self.sock.recv(1024)
            data += recv

        raw_token_data = data.decode("shift-jis").split("\n")[:-2] # Remove EOS and newline
        raw_token_data = [token for token in raw_token_data if token[0] != self.JUMAN_DISCARD_CHR]
        raw_tokens = [token.split(" ") for token in raw_token_data]
        return raw_tokens
        
    def is_kana(self, char):
        return ord(char) in self.KANA_LIST

    def strip_tail(self, chars, kana):
        "Strips hiragana tail from token."
        for i, c in enumerate(chars[::-1]):
            if utils.misc.is_kanji(c):
                break
        return chars[:-i], kana[:-i], chars[-i:]

    def is_kanji(self, token_characters):
        for chara in token_characters:
            if utils.misc.is_kanji(chara):
                return True
        return False

    def tokenize(self, text):
        if not self.dictionary:
            self.dictionary = DicFetcher()

        raw_tokens = self._query_juman(text)
        current_char = 0
        tokens = []
        for raw_token in raw_tokens:
            raw, kana, base, *_ = raw_token
            is_kanji = self.is_kanji(raw)
            stripped_kanji, stripped_kana, tail = self.strip_tail(raw, kana)
            english = self.dictionary.fetch_word(base)

            last_char_index = current_char+len(raw)
            current_char = last_char_index

            token = Token(raw, kana, stripped_kanji, stripped_kana, tail, base, english, is_kanji)
            tokens.append(token)

        self.dictionary.cur.close()
        self.dictionary.con.close()
        self.dictionary = None

        return tokens
