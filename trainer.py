from keras.callbacks import ModelCheckpoint
from data_wrangler import DataWrangler, CustomDataWrangler
from cnn import KanjiRecognizer
from cnn import ElementRecognizer
from cnn import ElementClassifier
from cnn import InceptionV3Model
import config


if __name__ == "__main__":
    CLASSES = 236
    NUM_TRAIN_SAMPLES = 30355#18881 #5160
    NUM_VAL_SAMPLES = 7572
    #cnn = KanjiRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    cnn = ElementClassifier(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    #cnn = InceptionV3Model(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    #cnn.load_model("CNN_ELEMENT_INC.10-0.257-2.280-0.660-0.915.h5")
    cnn.build_model()

    # cnn2 = InceptionV3Model(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    # cnn2.load_model("CNN_ELEMENT_INC.09-0.996-0.039-0.996-0.041.h5")
    # cnn.set_weights(cnn2.get_weights())
    # del cnn2

    dw = CustomDataWrangler(image_size=(64, 64), train_path="C:\\DatasetCache\\element_antialias_wb_modern\\train", val_path="C:\\DatasetCache\\element_antialias_wb_modern\\val")
    #dw = DataWrangler(image_size=(64, 64), train_path="C:\\DatasetCache\\element_antialias_wb_modern\\train", val_path="C:\\DatasetCache\\element_antialias_wb_modern\\val")

    def get_save_callback():
        model_name = "CNN_ELEMENTS_TRUNC_M7.{epoch:02d}-{val_acc:.3f}-{val_loss:.3f}-{acc:.3f}-{loss:.3f}.h5"
        return ModelCheckpoint(model_name, monitor='val_acc', verbose = 1, save_best_only = False)

    #class_weights = {0:34, 1: 1, 2: 34}

    train_gen = dw.get_train_generator()
    val_gen = dw.get_val_generator()
    for i in train_gen:
        print(type(i))
        print(i[0].shape, i[1].shape)
        break
    input()
    #print(type(train_gen))

    save_callback = get_save_callback()

    cnn.fit(
        train_gen,
        val_gen,
        NUM_TRAIN_SAMPLES/config.BATCH_SIZE,
        NUM_VAL_SAMPLES/config.BATCH_SIZE,
        [save_callback])