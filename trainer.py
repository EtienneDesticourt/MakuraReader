from keras.callbacks import ModelCheckpoint
from data_wrangler import DataWrangler, CustomDataWrangler, E2KGenerator
from cnn import KanjiRecognizer
from cnn import ElementRecognizer
from cnn import ElementClassifier
from cnn import InceptionV3Model
import config
from e2k_classifier import E2KClassifier


if __name__ == "__main__":
    CLASSES = 128
    NUM_TRAIN_SAMPLES = 120000#46197 ##7136#30355#18881 #5160
    NUM_VAL_SAMPLES = 15000#11528 ##1659#7572
    #cnn = KanjiRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    #cnn = ElementClassifier(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    #cnn = InceptionV3Model(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    #cnn.load_model(config.MODEL_TO_LOAD)
    #cnn.build_model()

    # cnn2 = InceptionV3Model(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    # cnn2.load_model("CNN_ELEMENT_INC.09-0.996-0.039-0.996-0.041.h5")
    # cnn.set_weights(cnn2.get_weights())
    # del cnn2

    #dw = CustomDataWrangler(image_size=(64, 64), train_path="C:\\DatasetCache\\all_kanjis_all_fonts_bw\\train", val_path="C:\\DatasetCache\\all_kanjis_all_fonts_bw\\val")

    # TEMP REMOVE FROM HERE ON 

    # Read kanji element decomposition dataset
    with open("data\\kanji_elements.txt", "r", encoding="utf8") as f:
        data = f.read().split("\n")
    while "" in data:
        data.remove("")
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
    remove_elements = []
    for i in elements:
        if len(elements[i]) < 15:
            remove_elements.append(i)
    for i in remove_elements:
        elements.pop(i)
        elements_ordered.remove(i)
    # TEMP REMOVE ABOVE  NO FURTHER



    classes = elements_ordered
    dw = DataWrangler(image_size=(64, 64), 
        train_path="C:\\DatasetCache\\all_kanjis_all_fonts_bw\\train", 
        val_path="C:\\DatasetCache\\all_kanjis_all_fonts_bw\\val")

    def get_save_callback():
        model_name = "CNN_E2K_TRUNC_M7.{epoch:02d}-{val_acc:.3f}-{val_loss:.3f}-{acc:.3f}-{loss:.3f}.h5"
        return ModelCheckpoint(model_name, monitor='val_acc', verbose = 1, save_best_only = False)

    #class_weights = {0:34, 1: 1, 2: 34}

    train_gen = dw.get_train_generator()
    val_gen = dw.get_val_generator()

    #e2k_train_gen = E2KGenerator(cnn, train_gen)
    #e2k_val_gen = E2KGenerator(cnn, val_gen)


    e2k = E2KClassifier(config.MODEL_TO_LOAD, config.LEARNING_RATE, config.EPOCHS)
    e2k.load_model("CNN_E2K_TRUNC_M7.03-0.000-7.859-0.000-7.827.h5")


    save_callback = get_save_callback()

    e2k.fit(
        train_gen,
        val_gen,
        NUM_TRAIN_SAMPLES,
        NUM_VAL_SAMPLES,
        [save_callback])