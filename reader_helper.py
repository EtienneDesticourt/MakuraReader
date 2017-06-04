from renderer import Renderer
from kindle_reader import KindleReader
from collections import namedtuple

Character = namedtuple('Character', ['segment', 'text'])

DEFAULT_READER = KindleReader
DEFAULT_RENDERER = Renderer
DEFAULT_RECOGNIZER = Recognizer

class ReaderHelper(object):

	def __init__(self, kindle_bbox, line_width, char_size_range, Reader=DEFAULT_READER, Renderer=DEFAULT_RENDERER, Recognizer=DEFAULT_RECOGNIZER):
		self.reader = Reader(kindle_bbox, line_width, char_size_range)
		image_size = self.reader.get_size()
		if self.reader.background_is_white():
			background = (255, 255, 255)
			text_color = (0, 0, 0)
		else:
			background = (0, 0, 0)
			text_color = (255, 255, 255)
		self.renderer = Renderer(image_size, line_width, background, text_color)
		self.recognizer = Recognizer()

	def draw(self):
		characters = [Character(segment, text="ka") for segment in self.reader.get_characters()]
		text = self.recognizer.classify(characters)
		tokens = self.tokenizer.tokenize(text, characters)
		image = self.renderer.render(characters, tokens)
		image.show()



if __name__ == "__main__":

	bbox = (212, 155, 655, 960)
	line_width = 45
	char_min_size = 26
	char_max_size = 32
	reader_helper = ReaderHelper(bbox, line_width, [char_min_size, char_max_size])
	reader_helper.draw()