import tinysegmenter
from collections import namedtuple
import re

Token = namedtuple('Token', ['characters', 'kana'])

DEFAULT_DIC_PATH = "data\\JMdict_e"

class Tokenizer():

	def __init__(self):
		self.words = {}

	def load_dictionary(self, dic_path=DEFAULT_DIC_PATH):
		with open(dic_path, "r", encoding="utf8") as f:
			data = f.read()
		entries = re.findall("<entry>.*?</entry>", data, flags=re.DOTALL)
		for entry in entries:
			kanjis = re.findall("<keb>(.*?)</keb>", entry, flags=re.DOTALL)
			kana = re.findall("<reb>(.*?)</reb>", entry, flags=re.DOTALL)
			for kanji in kanjis:
				self.words[kanji] = kana[0]

	def get_kana(self, text, characters):
		tokens_text = tinysegmenter.tokenize(text)
		current_char = 0
		tokens = []
		for text in tokens_text:
			kana = ""
			if text in self.words:
				kana = self.words[text]
			token = Token(characters=characters[current_char:current_char+len(text)], kana=kana)
			current_char += len(text)
			tokens.append(token)
		return tokens


if __name__ == "__main__":
	text = u"本書は実在する人気の深夜ラジオ番組を聴きながら、ひたむきに生きる人々の姿を描いた５つの短編集。深夜ラジオはとても独特な世界だ。人気のタレントたちが、普段テレビで見る姿とは異なり、かなり本音で話している。端正な顔立ちの福山雅治がエロトークを連発したり、いい人キャラのはずの関根勤が毒々しい発言をする逸話は有名だ。彼らのトークに笑い転げ、新しい音楽を知り、リスナーの失恋話に共感する。そんな深夜ラジオの想い出がある人なら、本書を読んで懐かしさを感じるかもしれない。"
	characters = [chara for chara in text]

	tokens = tinysegmenter.tokenize(text)

	tk = Tokenizer()
	tk.load_dictionary()
	tk.get_kana(text, characters)
	# print(len(tokens))
	# print(len(characters))
	# tk = Tokenizer()
	# tk.get_kana(text, characters)
