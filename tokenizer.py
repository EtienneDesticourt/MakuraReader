from collections import namedtuple
import socket
import time
from juman import juman_launcher


Token = namedtuple('Token', ['characters', 'kana'])


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
        for i, c in enumerate(chars):
            if self.is_kana(c):
                kana = kana[:-(len(chars)-i)]
                break
        return Token(characters=chars, kana=kana)

    def tokenize(self, text):
        raw_tokens = self._query_juman(text)
        return [self.strip_tail(chars, kana) for chars, kana, *_ in raw_tokens]
