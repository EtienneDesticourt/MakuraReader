import os
from naive_segmenter import NaiveSegmenter
from cnn import KanjiRecognizer
import numpy as np
import config

if __name__ == "__main__":


    # fonts = os.listdir("data\\train\\連")
    # fonts = [font.replace(".jpg","") for font in fonts]
    # print(fonts)

    #--------------

    # with open("kanjidic", "r", encoding="utf8") as f:
    #   for line in f.read().split("\n"):
            
    #--------------

    # top = "kanji_clusters2\\val"
    # for cluster in os.listdir(top):
    #   for f in os.listdir(os.path.join(top, cluster)):
    #       path = os.path.join(top, cluster, f)
    #       os.rename(path, path+".jpg")
            
    #--------------

    CLASSES = 3144
    KR = KanjiRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)    
    KR.load_model("models\\full1\\CNN_FULL.0.08-0.30.h5")

    bbox = (212, 155, 655, 950)
    line_width = 45
    char_min_size = 26
    char_max_size = 32
    NS = NaiveSegmenter(bbox, line_width, char_min_size, char_max_size)
    chars = NS.get_characters()

    result = ""
    for char in chars:
        image = np.array(char)[np.newaxis, :, :, :]
        kanjis = np.array(os.listdir("data3\\train"))
        answer = KR.predict(image)
        kanji_answer = kanjis[answer[0, :] != 0]
        if len(kanji_answer) > 0:
            kanji = kanji_answer[0]
            result += kanji
        # print(kanjis.shape)
        # print(answer[0, :].shape)
        # print(np.sum(answer[0, :]))

    with open("result.txt", "w", encoding="utf8") as f:
        f.write(result)
