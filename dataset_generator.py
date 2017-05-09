# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import config
import random
import time

if __name__ == "__main__":
    DEST_DIR_TRAIN = "data\\data4\\train"#config.VAL_DIR
    DEST_DIR_VAL = "data\\data4\\val"#config.VAL_DIR
    CLASS_FILE = "kanji.txt"
    FONTS = config.FONTS
    FONT_SIZES = config.FONT_SIZES
    IMAGE_FONTS = [ImageFont.truetype(font_file, font_size) for font_file in FONTS for font_size in FONT_SIZES]
    print("Loaded", len(IMAGE_FONTS), "font type and size combinations.")


    with open(CLASS_FILE, "r", encoding="utf8") as f:
        kanjis = f.read().split("\n")
    while "" in kanjis:
        kanjis.remove("")
    print("Found", len(kanjis), "kanjis.")

    for kanji in kanjis:
        train_path = os.path.join(DEST_DIR_TRAIN, kanji)
        val_path = os.path.join(DEST_DIR_VAL, kanji)
        if not os.path.exists(train_path):
            os.makedirs(train_path)
        if not os.path.exists(val_path):
            os.makedirs(val_path)
    print("Created kanji directories.")

    start = time.time()
    j = 0
    orig = Image.new("RGB", config.IMAGE_SIZE, config.BACKGROUND)
    for kanji in kanjis:
        i=0
        for font in IMAGE_FONTS:
            image = orig.copy()
            draw = ImageDraw.Draw(image)
            draw.text (config.TEXT_OFFSET, kanji, font=font, fill=config.COLOR)
            if random.random() >= config.TRAINING_PERCENT:
                directory = os.path.join(DEST_DIR_VAL, kanji)
            else:
                directory = os.path.join(DEST_DIR_TRAIN, kanji)
            file_path = os.path.join(directory, str(i) + ".jpg")#kanji + str(i) + ".jpg")
            image.save(file_path, "JPEG")
            i += 1
        j += 1
        if j % 500 == 0:
            end = time.time()
            start = time.time()
            print("Rendered", j, "kanjis out of", len(kanjis), "in", end-start, "seconds.")

    print("Done generating data.")
