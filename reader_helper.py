from renderer import Renderer
from kindle_reader import KindleReader
from collections import namedtuple
from recognizer import Recognizer
from tokenizer import Tokenizer

Character = namedtuple('Character', ['segment', 'text'])

DEFAULT_READER = KindleReader
DEFAULT_RENDERER = Renderer
DEFAULT_RECOGNIZER = Recognizer
DEFAULT_TOKENIZER = Tokenizer

DISCR_MODEL   = "weights\\CNN_K_M7_2_DISC.24-0.995-0.013.h5"
KAN_HI_MODEL  = "weights\\CNN_K_M7_2_KAN_HI.21-0.987-0.041.h5"
KATA_MODEL    = "weights\\CNN_K_M7_2_KATA.24-0.985-0.057.h5"
KAN_HI_LABELS = "weights\\kan_hi_labels.npy"
KATA_LABELS   = "weights\\kata_labels.npy"

class ReaderHelper(object):

	def __init__(self, kindle_bbox, line_width, char_size_range, Reader=DEFAULT_READER, Renderer=DEFAULT_RENDERER,
		Recognizer=DEFAULT_RECOGNIZER,
		Tokenizer=DEFAULT_TOKENIZER):
		self.reader = Reader(kindle_bbox, line_width, char_size_range)
		image_size = self.reader.get_size()
		if self.reader.background_is_white():
			background = (255, 255, 255)
			text_color = (0, 0, 0)
		else:
			background = (0, 0, 0)
			text_color = (255, 255, 255)
		self.tokenizer = Tokenizer()
		self.tokenizer.load_dictionary()
		self.renderer = Renderer(image_size, line_width, background, text_color)
		self.recognizer = Recognizer(DISCR_MODEL, KAN_HI_MODEL, KATA_MODEL, KAN_HI_LABELS, KATA_LABELS)

	def draw(self):
		characters = [Character(segment, text="ka") for segment in self.reader.get_characters()]
		text = self.recognizer.classify(characters)
		with open("tempresult.txt", "w", encoding="utf8") as f:
			f.write(text)
		tokens = self.tokenizer.get_kana(text, characters)
		image = self.renderer.render(characters, tokens)
		image.show()



if __name__ == "__main__":
	# TODO: Remove black characters 	X
	# TODO: Fix order					X
	# TODO: Create alphabet model 		X
	# TODO: Load katakana data			X
		# TODO: Commit to github        X
		# TODO: Remove comments 		X
		# TODO: Recommit to github		X
		# TODO: Make call with preprocess X
		# TODO: Load 1C and 9B and add    X
		# TODO: Make postprocessing call  X
	# TODO: Train alphabet model 		  X
	# TODO: Train for hira, kata 		  X
	# TODO: Recognize points and commas   X	
	# TODO: Clean files
	# TODO: Add GUI (electron)
	# TODO: Fix discriminator
	# TODO: Remove trailing characters
	# TODO: Add translator 
	# TODO: Improve kanji transcription 
	# TODO: Improve positionning
	# TODO: Added automated segmentation tuning
	# TODO: Prune model weights to improve memory footprint
	# TODO: Add element model
	# TODO: Integrate with makura japanese, save sentence samples
	# TODO: Makura japanese unlock skills, manually or through immersion (golden petals)


	bbox = (212, 155, 655, 960)
	line_width = 45
	char_min_size = 26
	char_max_size = 32
	reader_helper = ReaderHelper(bbox, line_width, [char_min_size, char_max_size])
	reader_helper.draw()