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
    DEST_DIR_TRAIN = "C:\\DatasetCache\\element_antialias_wb_modern_balanced_nobold\\train"#config.VAL_DIR
    DEST_DIR_VAL = "C:\\DatasetCache\\element_antialias_wb_modern_balanced_nobold\\val"#config.VAL_DIR
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
    elements_ordered = []
    kanjis = []
    kanji_elements = {}
    elements = {}
    for kanji in data:
        k, es = kanji.split(":")
        kanjis.append(k)
        kanji_elements[k] = es

        for e in es:
            if e not in elements:
                elements[e] = []
                elements_ordered.append(e)
            elements[e].append(k)


    # Only keep elements present in more than 15 kanjis
    remove_elements = []
    for i in elements:
        if len(elements[i]) < 15:
            remove_elements.append(i)
    for i in remove_elements:
        elements.pop(i)
        elements_ordered.remove(i)
    print("Found", len(elements), "elements.")

    def build_truth_vector(kanji):
        vector = [0]*len(elements_ordered)
        for element in kanji_elements[kanji]:
            if element in elements_ordered:
                i = elements_ordered.index(element)
                vector[i] = 1
        return vector

    kanji_labels = {}
    for kanji in kanjis:
        vector = build_truth_vector(kanji)
        kanji_labels[kanji] = vector



    #create_class_directories(elements, DEST_DIR_TRAIN, DEST_DIR_VAL)
    #print("Created class directories.")

    i = 0
    j = 0
    training_dataset = ""
    validation_dataset = ""
    start = time.time()
    orig = Image.new("RGB", config.IMAGE_SIZE, config.BACKGROUND)
    for element in elements:
        k = 0
        kanjis = elements[element]
        for font in IMAGE_FONTS:
            for kanji in kanjis:
                image = orig.copy()
                draw = ImageDraw.Draw(image)
                draw.text (config.TEXT_OFFSET, kanji, font=font, fill=config.COLOR)
                file_name = str(i) + ".jpg"
                if random.random() >= config.TRAINING_PERCENT:
                    file_path = os.path.join(DEST_DIR_VAL, file_name)
                    validation_dataset += file_name + "\t" + str(kanji_labels[kanji]) + "\n"
                else:
                    file_path = os.path.join(DEST_DIR_TRAIN, file_name)
                    training_dataset += file_name + "\t" + str(kanji_labels[kanji]) + "\n"
                image.save(file_path, "JPEG", quality=100)
                i += 1
                k += 1
                if k > 450:
                    break
            if k > 450:
                break
        j += 1
        if j % 10 == 0:
            end = time.time()
            print("Rendered", j, "elements out of", len(elements), "in", end-start, "seconds.")
            start = time.time()

    with open("training.csv", "w") as f:
        f.write(training_dataset)
    with open("validation.csv", "w") as f:
        f.write(validation_dataset)


