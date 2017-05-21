# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import config
import random
import time

KANJI_CLASSIFIER = "KANJI_CLASSIFIER"
ELEMENT_CLASSIFIER = "ELEMENT_CLASSIFIER"

def create_class_directories(classes, train_dir, val_dir):
    for label in classes:
        train_path = os.path.join(train_dir, label)
        val_path = os.path.join(val_dir, label)
        if not os.path.exists(train_path):
            os.makedirs(train_path)
        if not os.path.exists(val_path):
            os.makedirs(val_path)


if __name__ == "__main__":
    DEST_DIR_TRAIN = "C:\\DatasetCache\\element_antialias_wb\\train"#config.VAL_DIR
    DEST_DIR_VAL = "C:\\DatasetCache\\element_antialias_wb\\val"#config.VAL_DIR
    CLASS_FILE = "kanji.txt"
    FONTS = config.FONTS
    FONT_SIZES = config.FONT_SIZES
    IMAGE_FONTS = [ImageFont.truetype(font_file, font_size) for font_file in FONTS for font_size in FONT_SIZES]
    REMOVE_ANTIALIAS = False
    CLASSIFIER_TYPE = ELEMENT_CLASSIFIER
    print("Loaded", len(IMAGE_FONTS), "font type and size combinations.")


    # Read kanji element decomposition dataset
    with open("kanji_elements.txt", "r", encoding="utf8") as f:
        data = f.read().split("\n")
    while "" in data:
        data.remove("")

    # Create dictionnary of elements and their corresponding kanjis
    kanjis = []
    kanji_elements = {}
    elements = {}
    for kanji in data:
        k, es = kanji.split(":")
        kanjis.append(k)

        for e in es:
            if e not in elements:
                    elements[e] = []
            elements[e].append(k)

    # Only keep elements present in more than 15 kanjis
    remove_elements = []
    for i in elements:
        if len(elements[i]) < 15:
            remove_elements.append(i)
    for i in remove_elements:
        elements.pop(i)
    print("Found", len(elements), "elements.")

    create_class_directories(elements, DEST_DIR_TRAIN, DEST_DIR_VAL)
    print("Created class directories.")

    i = 0
    j = 0
    start = time.time()
    orig = Image.new("RGB", config.IMAGE_SIZE, config.BACKGROUND)
    dataset = ""
    for element in elements:
        kanjis = elements[element]
        for kanji in kanjis:
            font = IMAGE_FONTS[0]
            image = orig.copy()
            draw = ImageDraw.Draw(image)
            draw.text (config.TEXT_OFFSET, kanji, font=font, fill=config.COLOR)
            if random.random() >= config.TRAINING_PERCENT:
                directory = os.path.join(DEST_DIR_VAL, element)
            else:
                directory = os.path.join(DEST_DIR_TRAIN, element)
            file_name = str(i) + ".jpg"
            file_path = os.path.join(directory, file_name)
            image.save(file_path, "JPEG", quality=100)
            i += 1
        j += 1
        if j % 100 == 0:
            end = time.time()
            print("Rendered", j, "elements out of", len(elements), "in", end-start, "seconds.")
            start = time.time()

