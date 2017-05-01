# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os

if __name__ == "__main__":
	DIR = "data\\val"
	KANJI_LIST = "kanji.txt"
	FONT = "msgothic.ttc"
	FONT_SIZE = 15
	COLOR = (255, 255, 255)
	TEXT_OFFSET = (4, 2)
	IMG_SIZE = (25, 25)
	BACKGROUND = (0, 0, 0)

	with open(KANJI_LIST, "r", encoding="utf8") as f:
		kanjis = f.read().split("\n")

	while "" in kanjis:
		kanjis.remove("")

	for kanji in kanjis:
		image = Image.new("RGB", IMG_SIZE, BACKGROUND)
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype(FONT, FONT_SIZE)
		draw.text (TEXT_OFFSET, kanji, font=font, fill=COLOR)
		file_path = os.path.join(DIR, kanji + ".jpg")
		image.save(file_path, "JPEG")

	print("Done generating data.")
