

class Token(object):
	"A single lexical unit."

	def __init__(self, raw, kana, stripped, base, english, is_kanji, characters):
		self.raw        = raw
		self.kana       = kana
		self.stripped   = stripped
		self.base       = base
		self.english    = english
		self.is_kanji   = is_kanji
		self.characters = characters
		self.x, self.y = self.characters[0].x, self.characters[0].y
		self.width  = self.characters[0].width
		self.height = sum([char.height for char in self.characters])
