import tinysegmenter
from collections import namedtuple
import re
import socket
import time
from juman import juman_launcher

Token = namedtuple('Token', ['characters', 'kana'])

DEFAULT_DIC_PATH = "data\\JMdict_e"

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

    def tokenize(self, text):
        # TODO: add timeout
        self.sock.sendall((text+"\n").encode("shift-jis"))
        data = b""
        while b"EOS" not in data:
            recv = self.sock.recv(1024)
            data += recv

        tokens_data = data.decode("shift-jis").split("\n")
        tokens_data.pop() # Remove EOS
        tokens_data.pop() # Remove new line

        tokens_data = [token for token in tokens_data if token[0] != self.JUMAN_DISCARD_CHR]

        with open("tokens.txt", "w", encoding="utf8") as f:
            f.write("\n".join(tokens_data))

        tokens = []
        for line in tokens_data:
            data = line.split(" ")
            token = data[0]
            kana = data[1]
            tokens.append((token, kana))

        return tokens
        
    def is_kana(self, char):
        return ord(char) in self.KANA_LIST

    def strip_tail(self, token):
        "Strips hiragana tail from token."
        text, kana = token
        head = kana
        for i, c in enumerate(text):
            if self.is_kana(c):
                head = kana[:-(len(text)-i)]
                break
        return (text, head)

    def get_kana(self, text, characters):
        token_data = self.tokenize(text)
        token_data = [self.strip_tail(token) for token in token_data]
        current_char = 0
        tokens = []
        for text, kana in token_data:
            if len(kana) != 0:
                # print(current_char, current_char+len(text))
                characters2 = characters[current_char:current_char+len(text)]
                # print(len(characters2))
                token = Token(characters=characters2, kana=kana)
                tokens.append(token)
            current_char += len(text)
        return tokens


if __name__ == "__main__":
    text = u"本書は実在する人気の深夜ラジオ番組を聴きながら、ひたむきに生きる人々の姿を描いた５つの短編集。深夜ラジオはとても独特な世界だ。人気のタレントたちが、普段テレビで見る姿とは異なり、かなり本音で話している。端正な顔立ちの福山雅治がエロトークを連発したり、いい人キャラのはずの関根勤が毒々しい発言をする逸話は有名だ。彼らのトークに笑い転げ、新しい音楽を知り、リスナーの失恋話に共感する。そんな深夜ラジオの想い出がある人なら、本書を読んで懐かしさを感じるかもしれない。"
    text = u"本書は実在する人気の深夜ラジオ番組を聴きながら。"


    # import socket, re
    # import jaconv

    # #text = jaconv.h2z(text, kana=True, ascii=True, digit=True)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(('localhost', 32000))
    # sock.send(b"RUN -e2\n")
    # data = b""
    # while b"OK" not in data:
    #     data = sock.recv(1024)
    #     print(data)

    # print("hey")
    # print(len(text))

    # sock.sendall((text+"\n").encode("shift-jis"))
    # data = sock.recv(1024)
    # print(data)
    # recv = b"hello"
    # while b"EOS" not in data:
    #     recv = sock.recv(1024)
    #     print("mmm")

    #     data += recv

    # with open("temp_results2.txt", "a", encoding="utf8") as f:
    #     f.write(data.decode("shift-jis"))
    #     print("bam")

    # sock.close()
    # input()


    # characters = [chara for chara in text]

    # tokens = tinysegmenter.tokenize(text)

    # tk = Tokenizer()
    # tk.load_dictionary()
    # tk.get_kana(text, characters)
    # print(len(tokens))
    # print(len(characters))
    # tk = Tokenizer()
    # tk.get_kana(text, characters)
