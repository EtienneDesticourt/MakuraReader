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
    DEST_DIR_TRAIN = "C:\\DatasetCache\\data10\\train"#config.VAL_DIR
    DEST_DIR_VAL = "C:\\DatasetCache\\data10\\val"#config.VAL_DIR
    CLASS_FILE = "kanji.txt"
    FONTS = config.FONTS
    FONT_SIZES = config.FONT_SIZES
    IMAGE_FONTS = [ImageFont.truetype(font_file, font_size) for font_file in FONTS for font_size in FONT_SIZES]
    REMOVE_ANTIALIAS = True
    CLASSIFIER_TYPE = ELEMENT_CLASSIFIER
    print("Loaded", len(IMAGE_FONTS), "font type and size combinations.")

    # Read kanji dataset
    with open(CLASS_FILE, "r", encoding="utf8") as f:
        kanjis = f.read().split("\n")
    while "" in kanjis:
        kanjis.remove("")
    print("Found", len(kanjis), "kanjis.")

    # Read kanji element decomposition dataset
    kanji_elements = {}
    with open("kanji_elements.txt", "r", encoding="utf8") as f:
        data = f.read().split("\n")
    while "" in data:
        data.remove("")

    elements = []
    for line in data:
        k, e = line.split(":")
        kanji_elements[k] = e
        for char in e:
            if char not in elements:
                elements.append(char)
    print("Found", len(elements), "elements.")

    
    # create_class_directories(kanjis, DEST_DIR_TRAIN, DEST_DIR_VAL) # Uncomment for kanji classifier
    create_class_directories(elements, DEST_DIR_TRAIN, DEST_DIR_VAL)
    print("Created class directories.")


    start = time.time()
    j = 0
    i=0
    orig = Image.new("RGB", config.IMAGE_SIZE, config.BACKGROUND)
    for kanji in kanjis:
        images = []

        # Draw kanji
        for font in IMAGE_FONTS:
            image = orig.copy()
            draw = ImageDraw.Draw(image)
            draw.text (config.TEXT_OFFSET, kanji, font=font, fill=config.COLOR)
            if REMOVE_ANTIALIAS:
                image = image.convert('L')
                image = image.point(lambda x: 0 if x < 128 else 255, '1')
            images.append(image)            

        # Save kanjis (complexity and memory usage outset by clarity of code)
        if CLASSIFIER_TYPE == KANJI_CLASSIFIER:
            for image in images:                          
                if random.random() >= config.TRAINING_PERCENT:
                    directory = os.path.join(DEST_DIR_VAL, kanji)
                else:
                    directory = os.path.join(DEST_DIR_TRAIN, kanji)
                file_path = os.path.join(directory, str(i) + ".jpg")#kanji + str(i) + ".jpg")
                image.save(file_path, "JPEG", quality=100)
                i += 1

        elif CLASSIFIER_TYPE == ELEMENT_CLASSIFIER:
            for image in images:       
                for element in kanji_elements[kanji]:
                    if random.random() >= config.TRAINING_PERCENT:
                        directory = os.path.join(DEST_DIR_VAL, element)
                    else:
                        directory = os.path.join(DEST_DIR_TRAIN, element)

                    file_path = os.path.join(directory, str(i) + ".jpg")#kanji + str(i) + ".jpg")
                    image.save(file_path, "JPEG", quality=100)
                    i += 1

        j += 1
        if j % 100 == 0:
            end = time.time()
            print("Rendered", j, "kanjis out of", len(kanjis), "in", end-start, "seconds.")
            start = time.time()

    print("Done generating data.")
