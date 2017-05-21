import os
from naive_segmenter import NaiveSegmenter
from cnn import KanjiRecognizer
from cnn import ElementRecognizer, ElementClassifier
import numpy as np
import config
from PIL import Image
import random
import uuid
from keras.preprocessing.image import ImageDataGenerator

if __name__ == "__main__":


    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
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

    # CLASSES = 236
    # KR = ElementRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    # #KR = KanjiRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)    
    # KR.load_model("CNN_ELEMENT_INC.08-0.996-0.041-0.996-0.044.h5")

    # bbox = (212, 155, 655, 950)
    # line_width = 45
    # char_min_size = 26
    # char_max_size = 32
    # NS = NaiveSegmenter(bbox, line_width, char_min_size, char_max_size)
    # #chars = NS.get_characters()

    # result = ""
    # for image in os.listdir("data\\images"):# in chars:
    #     char = Image.open(os.path.join("data\\images", image))
    #     #char.show()
    #     char = char.resize((150, 150))
    #     char.show()
    #     image = np.array(char)[np.newaxis, :, :, :]
    #     #kanjis = np.array(os.listdir("C:\\DatasetCache\\data10\\train"))
    #     elements = np.array(os.listdir("C:\\DatasetCache\\element_antialias_one_font_wb\\train"))
    #     answer = KR.predict(image)
    #     print(answer)
    #     input()
    #     elements_present = elements[answer[0, :] != 0]
    #     if len(elements_present) > 0:
    #         kanji = str(elements_present)#kanjis[answer[0, :].argmax()]# 
    #         result += kanji + "\n"#str(kanji_answer) + "\n" #kanji + "\n"


    #     # with open("result.txt", "w", encoding="utf8") as f:
    #     #     f.write(result)
    # #     # print(kanjis.shape)
    # #     # print(answer[0, :].shape)
    # #     # print(np.sum(answer[0, :]))

    # with open("result.txt", "w", encoding="utf8") as f:
    #     f.write(result)
            
    #--------------

    #Count kanjis per elements

    # with open("kanji_elements.txt", "r", encoding="utf8") as f:
    #     data = f.read().split("\n")

    # kanjis = []
    # elements = {}
    # for kanji in data:
    #     k, es = kanji.split(":")
    #     kanjis.append(k)

    #     for e in es:
    #         if e not in elements:
    #                 elements[e] = []
    #         elements[e].append(k)


    # count = {}

    # for i in range(200):
    #     count[i] = 0

    # for e in elements:
    #     if len(elements[e]) in count:
    #             count[len(elements[e])] += 1

    # #for c in count:
    #     #print(c, count[c])
    # j = 0
    # seen = []
    # for i in elements:
    #     if len(elements[i]) > 15:
    #         print(j, len(elements[i]))
    #         for kanji in elements[i]:
    #             if kanji not in seen:
    #                 seen.append(kanji)

    #         j += 1

    # unseen = 0
    # for kanji in kanjis:
    #     if kanji not in seen:
    #         unseen += 1

    # print("not seen", unseen)

    # a = [len(elements[i]) for i in elements]
    # print(max(a))

    # TODO:

    # new generation script only 144 elements
    # generate augmented to fill 160 images per example minimum
    # truncate rest at 160

  #--------------

    # CLASSES = 236
    # DATASET = "C:\\DatasetCache\\element_antialias_one_font_wb\\train"
    # MODEL = "CNN_ELEMENT_INC.08-0.996-0.041-0.996-0.044.h5"
    # IM_SIZE = (150, 150)
    # KR = ElementRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    # KR.load_model(MODEL)

    # classes = np.array(os.listdir(DATASET))

    # classes_accuracy = []
    # for label in classes:
    #     directory = os.path.join(DATASET, label)
    #     images = os.listdir(directory)
    #     correct = 0
    #     total = len(images)
    #     if total == 0: continue
    #     for image in images:
    #         image = Image.open(os.path.join(directory, image))
    #         image = image.resize(IM_SIZE)
    #         image = np.array(image)[np.newaxis, :, :, :]
    #         answer = KR.predict(image)
    #         elements_present = classes[answer[0, :] != 0]
    #         if label in elements_present:
    #             correct += 1
    #     accuracy = correct / total
    #     classes_accuracy.append(correct / total)
    #     print(accuracy)

    # with open("results.txt", "w", encoding="utf8") as f:
    #     result = ""
    #     for acc in classes_accuracy:
    #         result += label + ":" + str(acc) + "\n"
    #     f.write(result)


  #--------------

  # Equalize number of images for each class
    # DATASET = "C:\\DatasetCache\\element_antialias_wb\\train"
    # NUM_IM = 160
    


    # j = 0
    # for label in os.listdir(DATASET):
    #     print(j)
    #     j += 1
    #     label_directory = os.path.join(DATASET, label)
    #     images = os.listdir(label_directory)
    #     # If too many images, remove the excess
    #     if len(images) > NUM_IM:
    #         kept_images = random.sample(images, NUM_IM)
    #         for image in images:
    #             if image not in kept_images:
    #                 image_path = os.path.join(label_directory, image)
    #                 os.remove(image_path)

    #     elif len(images) < NUM_IM:
    #         i = len(images)

    #         while i < NUM_IM:
    #             image = random.choice(images)
    #             im = Image.open(os.path.join(label_directory, image))
    #             new_path = os.path.join(label_directory, str(uuid.uuid4())+".jpg")
    #             im.save(new_path, quality=100)

    #             i += 1



    # CLASSES = 128
    # DATASET = "C:\\DatasetCache\\element_antialias_wb\\train"
    # MODEL = "CNN_ELEMENTS_TRUNC_M7.04-0.992-0.048-0.992-0.049.h5"
    # IM_SIZE = (64, 64)
    # KR = ElementClassifier(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    # KR.load_model(MODEL)

    # classes = np.array(os.listdir(DATASET))

    # for label in classes:


    # dw = DataWrangler(image_size=(64, 64), train_path="C:\\DatasetCache\\element_antialias_wb\\train", val_path="C:\\DatasetCache\\element_antialias_wb\\val")


    # image = Image.open("E:\\Users\\Etienne2\\Desktop\\7468.jpg").convert('L')
    # image = np.array(image)[np.newaxis, :, :, np.newaxis]
    # print(image)
    # answer = KR.predict(image)
    # print(answer)

    # classes_accuracy = []
    # for label in classes:
    #     directory = os.path.join(DATASET, label)
    #     images = os.listdir(directory)
    #     correct = 0
    #     total = len(images)
    #     if total == 0: continue
    #     for image in images:
    #         image = Image.open(os.path.join(directory, image))
    #         image = image.resize(IM_SIZE)
    #         image = np.array(image)[np.newaxis, :, :, :]
    #         answer = KR.predict(image)
    #         elements_present = classes[answer[0, :] != 0]
    #         if label in elements_present:
    #             correct += 1
    #     accuracy = correct / total
    #     classes_accuracy.append(correct / total)
    #     print(accuracy)

    # with open("results.txt", "w", encoding="utf8") as f:
    #     result = ""
    #     for acc in classes_accuracy:
    #         result += label + ":" + str(acc) + "\n"
    #     f.write(result)

    import numpy as np
    from data_wrangler import DataWrangler
    dw = DataWrangler(image_size=(64, 64), train_path="C:\\DatasetCache\\element_antialias_wb\\train", val_path="C:\\DatasetCache\\element_antialias_wb\\val")

    train_gen = dw.get_train_generator()

    values = 0
    nonzero = 0
    for i in train_gen:
        for j in i[1]:
            nonzero += np.sum(j)
            values += 1
        print(values, nonzero)