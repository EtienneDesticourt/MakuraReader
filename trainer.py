from keras.callbacks import ModelCheckpoint
from data_wrangler import DataWrangler
from cnn import KanjiRecognizer
import config


if __name__ == "__main__":
    NUM_TRAIN_SAMPLES = 5160#188818
    cnn = KanjiRecognizer(config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
    cnn.build_model()

    dw = DataWrangler()


    def get_save_callback(aug):
        model_name = "CNN." + str(aug) + ".{epoch:02d}-{val_acc:.2f}.h5"
        return ModelCheckpoint(model_name, monitor='val_acc', verbose = 1, save_best_only = True)

    for aug in range(config.NUM_AUGMENTATIONS):
        train_gen = dw.get_train_generator()
        val_gen = dw.get_val_generator()

        save_callback = get_save_callback(aug)

        #model.reset()
        cnn.fit(
            train_gen,
            val_gen,
            NUM_TRAIN_SAMPLES,
            dw.num_val_samples,
            [save_callback])