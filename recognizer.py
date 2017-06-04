from PIL import Image


class Recognizer(object):

	def __init__(self, image_size=(64, 64), background=(0, 0, 0)):
		self.image_size = image_size
		self.background = background

	def predict(self, image):
		return ""

	def classify(self, characters):
        image = Image.new("RGB", self.image_size, self.background)
        full_text = ""
		for character in characters:
			char_image = image.copy()
			char_image.paste(character.segment.image)
			char_text = self.predict(char_image)
			full_text += char_text
		return full_text