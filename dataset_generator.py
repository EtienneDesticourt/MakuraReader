# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import config

if __name__ == "__main__":
    DEST_DIR = "data3\\train"#config.VAL_DIR
    FONTS = config.FONTS
    IMAGE_FONTS = [ImageFont.truetype(font_file, config.FONT_SIZE) for font_file in FONTS]

    with open(config.KANJI_LIST, "r", encoding="utf8") as f:
        kanjis = f.read().split("\n")

    while "" in kanjis:
        kanjis.remove("")

    for kanji in kanjis:
        directory = os.path.join(DEST_DIR, kanji)
        if not os.path.exists(directory):
            os.makedirs(directory)

    import time

    start = time.time()



    j = 0
    orig = Image.new("RGB", config.IMAGE_SIZE, config.BACKGROUND)
    for kanji in kanjis:
        directory = os.path.join(DEST_DIR, kanji)
        i=0
        for font in IMAGE_FONTS:
            image = orig.copy()
            draw = ImageDraw.Draw(image)
            draw.text (config.TEXT_OFFSET, kanji, font=font, fill=config.COLOR)
            file_path = os.path.join(directory, str(i) + ".jpg")#kanji + str(i) + ".jpg")
            image.save(file_path, "JPEG")
            i += 1
        j += 1
        if j % 500 == 0:
            end = time.time()
            print(end - start)
            start = time.time()
            print(j)


    print("Done generating data.")
