from segmenter import Segmenter
from PIL import ImageGrab
from PIL import ImageDraw
import math

class NaiveSegmenter(Segmenter):

	def __init__(self, text_bounding_box, line_width, char_min_size, char_max_size):
		self.text_bounding_box = text_bounding_box
		self.line_width = line_width
		self.char_min_size = char_min_size
		self.char_max_size = char_max_size
		self.too_big_rectifier = 10

	def get_screen_capture(self):
		# TODO: LINUX
		return ImageGrab.grab(self.text_bounding_box)

	def get_segmentation_visualization(self):
		im = self.get_screen_capture()
		rgb_im = im.convert('RGB')
		width, height = im.size
		for x in range(0, width, self.line_width):
			top = 0
			left = x
			down = height
			right = x + self.line_width

			# Draw line
			draw = ImageDraw.Draw(im)
			draw.rectangle((left, top, right, down))

			def check_interesects_character(line_height):
				for x2 in range(left, right):
					if x2 >= im.size[0] or line_height >= im.size[1]:
						continue
					# Non background pixel detected = go down a pixel and check again
					if rgb_im.getpixel((x2, line_height)) != (0, 0, 0):
						return True
				return False

			line_height = 0
			last_line_drawn = 0
			last_was_too_big = False
			while line_height < im.size[1]:
				intersects_character = True
				size_too_small = True
				size_too_big = False
				while not size_too_big and (intersects_character or size_too_small):
					line_height += 1
					char_height = line_height - last_line_drawn
					if last_was_too_big:
						size_too_small = char_height < self.char_min_size - self.too_big_rectifier
					else:
						size_too_small = char_height < self.char_min_size

					size_too_big = char_height > self.char_max_size
					if not size_too_small:
						intersects_character = check_interesects_character(line_height)

				last_was_too_big = size_too_big
				draw.line((left, line_height, right, line_height))
				last_line_drawn = line_height




			# for y in range(0, height, self.character_size):
			# 	offset = int((y / self.character_size) * 0.4)
			# 	line_height = y  + offset
			# 	original_line_height = line_height

			# 	while True:
			# 		intersects_character = False
			# 		for x2 in range(left, right):
			# 			if x2 >= im.size[0] or line_height >= im.size[1]:
			# 				continue
			# 			# Non background pixel detected = go down a pixel and check again
			# 			if rgb_im.getpixel((x2, line_height)) != (0, 0, 0):
			# 				intersects_character = True
			# 				line_height += 1
			# 				if line_height >= im.size[1]:
			# 					intersects_character = False
			# 				break
			# 		if not intersects_character:
			# 			break

			# 	draw.line((left, line_height, right, line_height))
			# 	#draw.rectangle((left, y, right, y+self.character_size+ offset))


		im.show()


	def get_characters(self):
		characters = []
		line_characters = []
		temp = ""
		im = self.get_screen_capture()
		rgb_im = im.convert('RGB')
		width, height = im.size
		for x in range(0, width, self.line_width):
			top = 0
			left = x
			down = height
			right = x + self.line_width

			def check_interesects_character(line_height):
				for x2 in range(left, right):
					if x2 >= width or line_height >= height:
						continue
					# Non background pixel detected = go down a pixel and check again
					if rgb_im.getpixel((x2, line_height)) != (0, 0, 0):
						return True
				return False

			line_height = 0
			last_line_drawn = 0
			last_was_too_big = False
			while line_height < height:
				intersects_character = True
				size_too_small = True
				size_too_big = False
				while not size_too_big and (intersects_character or size_too_small):
					line_height += 1
					char_height = line_height - last_line_drawn
					if last_was_too_big:
						size_too_small = char_height < self.char_min_size - self.too_big_rectifier
					else:
						size_too_small = char_height < self.char_min_size

					size_too_big = char_height > self.char_max_size
					if not size_too_small:
						intersects_character = check_interesects_character(line_height)


				character = im.crop((left, last_line_drawn, right, line_height))
				line_characters.append(character)
				# if char_height > 30:
				# 	temp += str(line_height - last_line_drawn) + "\n"
				last_line_drawn = line_height
				last_was_too_big = size_too_big

			# We do top down but left to right
			# So we reverse the vertical line so it's fully reversed:
			# down top, left right and we can reverse the total at the end
			characters += reversed(line_characters) 
			line_characters = []


		i = 0
		for char in reversed(characters):
			char.save("images\\" + str(i) + ".jpg")
			i += 1

		# with open("temp.txt", "w") as f:
		# 	f.write(temp)

		# im = self.get_screen_capture()
		# width, height = im.size
		# num_lines = math.ceil(width / self.line_width)
		# print(num_lines)
		# for x in range(0, width, self.line_width):
		# 	line_pic = im.crop((x, 0, x+self.line_width, height))
		# 	print(line_pic.size)
		# 	line_pic.save(str(x) + ".jpg")


if __name__ == "__main__":
	bbox = (212, 155, 655, 950)
	line_width = 45
	char_min_size = 26
	char_max_size = 32
	NS = NaiveSegmenter(bbox, line_width, char_min_size, char_max_size)
	NS.get_segmentation_visualization()
	NS.get_characters()

