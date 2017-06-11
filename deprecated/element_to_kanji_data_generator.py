import numpy as np
from cnn import ElementClassifier
import os
import config
from data_wrangler import DataWrangler, CustomDataWrangler

# # Load kanjis
# KANJI_FILE = "data\\kanji.txt"

# with open(KANJI_FILE, "r", encoding="utf8") as f:
#     kanjis = f.read().split("\n")

# # Load fonts
# IMAGE_FONTS = [ImageFont.truetype(font_file, font_size) for font_file in config.FONTS for font_size in config.FONT_SIZES]


# orig = Image.new("RGB", config.IMAGE_SIZE, config.BACKGROUND)
# for kanji in kanjis:
#     for font in IMAGE_FONTS:
#         image = orig.copy()
#         draw = ImageDraw.Draw(image)
#         draw.text (config.TEXT_OFFSET, kanji, font=font, fill=config.COLOR)
#         image = image.convert('L')

DEST_DIR_TRAIN = "C:\\DatasetCache\\all_kanjis_all_fonts_bw\\train"#config.VAL_DIR

kanjis = os.listdir(DEST_DIR_TRAIN)

dw = DataWrangler(image_size=(64, 64), train_path=DEST_DIR_TRAIN, val_path="C:\\DatasetCache\\all_kanjis_all_fonts_bw\\val")

train_gen = dw.get_train_generator()


cnn = ElementClassifier(2500, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
cnn.load_model(config.MODEL_TO_LOAD)

elements = np.empty((0, 128), int)
labels = np.empty((0, 2500), int)

i = 0
with open("elements.out", "ba") as elements_file:
    with open("labels.out", "ba") as labels_file:
        for batch_images, batch_labels in train_gen:
            predictions = cnn.predict(batch_images)
            elements = np.vstack([elements, predictions])
            labels = np.vstack([labels, batch_labels])
            if elements.shape[0] >= 15000:
                np.savetxt(elements_file, elements)
                np.savetxt(labels_file, labels)                    
                elements = np.empty((0, 128), int)
                labels = np.empty((0, 2500), int)
                print(i)
            i += config.BATCH_SIZE
            if i > 150000:
                break


np.savetxt(elements_file, elements)
np.savetxt(labels_file, labels)    