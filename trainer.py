from keras.callbacks import ModelCheckpoint
from data_wrangler import DataWrangler
from cnn import KanjiRecognizer
import config


if __name__ == "__main__":
    CLASSES = 3144
    NUM_TRAIN_SAMPLES = 314400 #18881 #5160
    cnn = KanjiRecognizer(CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    cnn.build_model()

    dw = DataWrangler(train_path="data3\\train", val_path="data3\\val")

    def get_save_callback(aug):
        model_name = "CNN_FULL." + str(aug) + ".{epoch:02d}-{val_acc:.2f}.h5"
        return ModelCheckpoint(model_name, monitor='val_acc', verbose = 1, save_best_only = False)

    for aug in range(config.NUM_AUGMENTATIONS):
        train_gen = dw.get_train_generator()
        val_gen = dw.get_val_generator()

        save_callback = get_save_callback(aug)

        cnn.fit(
            train_gen,
            val_gen,
            NUM_TRAIN_SAMPLES,
            dw.num_val_samples,
            [save_callback])