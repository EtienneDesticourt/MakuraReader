from PIL import ImageGrab
import numpy as np
from naive_segmenter import NaiveSegmenter

PAGE_CHANGE_THRESHOLD = 1
DEFAULT_SEGMENTER = NaiveSegmenter

class KindleReader(object):

	def __init__(self, kindle_bbox, line_width, char_size_range, page_change_threshold=PAGE_CHANGE_THRESHOLD, Segmenter=DEFAULT_SEGMENTER):
		self.kindle_bbox = kindle_bbox
		self.line_width = line_width
		self.char_size_range = char_size_range
		self.last_capture = None
		self.page_change_threshold = page_change_threshold
		self.segmenter = Segmenter(kindle_bbox, line_width, char_size_range[0], char_size_range[1])
		
	def get_size(self):
		return self.capture_kindle().size # Could be more efficient but eh

	def get_lines(self):
		return self.segmenter.get_lines()

	def get_characters(self):
		return self.segmenter.get_characters()

	def capture_kindle(self):
		# TODO: LINUX
		return ImageGrab.grab(self.kindle_bbox)

	def background_is_white(self):
		# TODO: IMPLEMENT
		return False

	def page_has_changed(self):
		new_capture = self.capture_kindle()

		if self.last_capture == None:
			self.last_capture = new_capture
			return True

		array1 = np.array(new_capture.getdata())
		array2 = np.array(self.last_capture.getdata())

		self.last_capture = new_capture

		return np.sum(abs(array2-array1)) != 0


if __name__ == "__main__":
	import time
	bbox = (212, 155, 655, 950)
	line_width = 45
	char_min_size = 26
	char_max_size = 32
	KR = KindleReader(bbox, line_width, [char_min_size, char_max_size])
	while 1:
		print(KR.page_has_changed())
		time.sleep(2)