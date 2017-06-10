import os
import sklearn.utils
import sklearn.model_selection
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

from utils.ectl_loader import load_data
from models.cnn_classifiers import M7_2, alphabet_classifier
from keras.utils import np_utils
import numpy as np

from utils.misc import kanji_to_alphabet


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" # Disable warnings
DATASET_PATH = "data\\ETL9B\\ETL9B_1"
TEST_SPLIT_PERCENTAGE = 0.2
NUM_CLASSES = 3
NUM_EPOCHS = 25
BATCH_SIZE = 32

FILE_PATHS = ["data\\ETL9B\\ETL9B_1",
              "data\\ETL9B\\ETL9B_2",
              "data\\ETL9B\\ETL9B_3",
              "data\\ETL9B\\ETL9B_4"] # Keep 5th for testing


print("Compiling model.")
#model = M7_2(n_output=NUM_CLASSES, input_shape=(64, 64, 1))
model = load_model("CNN_K_M7_2_A.06-0.996-0.010.h5")
#model = alphabet_classifier("CNN_K_M7_2.21-0.987-0.041.h5")


for path in FILE_PATHS[3:]:
    print("Loading ECTL data.", path)
    x, y = load_data(path, truncate=10000, alphabet=True, verbose=True)
    

    print("Shuffling data.")
    x_shuffled, y_shuffled = sklearn.utils.shuffle(x, y, random_state=0)
    del x
    del y

    # print("Splitting train and test data.")
    # x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x_shuffled, y_shuffled, test_size=TEST_SPLIT_PERCENTAGE, random_state=42)
    # del x_shuffled
    # del y_shuffled

    def get_save_callback():
            model_name = "CNN_K_M7_2_A.{epoch:02d}-{acc:.3f}-{loss:.3f}.h5"
            return ModelCheckpoint(model_name, monitor='acc', verbose=1, save_best_only=False)


    print("Training model.")
    model.fit(x_shuffled, y_shuffled,
              epochs=NUM_EPOCHS,
              batch_size=BATCH_SIZE,
              callbacks= [get_save_callback()])

    del x_shuffled
    del y_shuffled

# save_model_weights('weights/M7_2-kanji_weights.h5', model)

# print("Evaluating model.")
# score, acc = model.evaluate(x_test, y_test,
#                             batch_size=128,
#                             verbose=0)

# print( "Training size: ", x_train.shape[0])
# print( "Test size: ", x_test.shape[0])
# print( "Test Score: ", score)
# print( "Test Accuracy: ", acc)
