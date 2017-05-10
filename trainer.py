from keras.callbacks import ModelCheckpoint
from data_wrangler import DataWrangler
from cnn import KanjiRecognizer
from cnn import ElementRecognizer
import config


if __name__ == "__main__":
    CLASSES = 236
    NUM_TRAIN_SAMPLES = 732000#18881 #5160
    #cnn = KanjiRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    #cnn.load_model("models\\kanji_only_2fc\\CNN_FULL.01-0.980.h5")
    cnn = ElementRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    cnn.build_model()

    dw = DataWrangler(train_path="C:\\DatasetCache\\data10\\train", val_path="C:\\DatasetCache\\data10\\val")

    def get_save_callback():
        model_name = "CNN_ELEMENT_FULL.{epoch:02d}-{val_acc:.3f}.h5"
        return ModelCheckpoint(model_name, monitor='val_acc', verbose = 1, save_best_only = False)

    #class_weights = {0:34, 1: 1, 2: 34}

    train_gen = dw.get_train_generator()
    val_gen = dw.get_val_generator()

    save_callback = get_save_callback()

    cnn.fit(
        train_gen,
        val_gen,
        NUM_TRAIN_SAMPLES,
        dw.num_val_samples,
        [save_callback])