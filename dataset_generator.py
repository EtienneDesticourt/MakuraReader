# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import config

if __name__ == "__main__":
    DEST_DIR = "data3\\val"#config.VAL_DIR
    FONT = config.FONT_ARIAL

    with open(config.KANJI_LIST, "r", encoding="utf8") as f:
        kanjis = f.read().split("\n")

    while "" in kanjis:
        kanjis.remove("")

    j = 0
    for kanji in kanjis:
        #print(kanji)
        i=0
        for font_file in config.VAL_FONTS:
            image = Image.new("RGB", config.IMAGE_SIZE, config.BACKGROUND)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font_file, config.FONT_SIZE)
            draw.text (config.TEXT_OFFSET, kanji, font=font, fill=config.COLOR)
            directory = os.path.join(DEST_DIR, kanji)
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_path = os.path.join(directory, font_file + ".jpg")#kanji + str(i) + ".jpg")

            image.save(file_path, "JPEG")
            i += 1
        j += 1
        if j % 100 == 0:
            print(j)


    print("Done generating data.")
