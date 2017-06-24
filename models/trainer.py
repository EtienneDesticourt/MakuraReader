import os
import sklearn.utils
import sklearn.model_selection
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
import numpy as np

from utils.ectl_loader import load_data
from utils.misc import jis_code_to_alphabet, get_simple_image_processer, JIS_201_to_208, get_kata_image_processor, jis_code_to_categorical
from utils.record_9B import Record9B
from utils.record_1C import Record1C
from models.cnn_classifiers import M7_2, alphabet_classifier

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" # Disable warnings
DATASET_PATH = "data\\ETL9B\\ETL9B_1"
TEST_SPLIT_PERCENTAGE = 0.2
NUM_EPOCHS = 10
BATCH_SIZE = 32
IMAGE_SIZE = (64, 64)

ETL9_PATHS = ["data\\ETL9B\\ETL9B_1",
              "data\\ETL9B\\ETL9B_2",
              "data\\ETL9B\\ETL9B_3",
              "data\\ETL9B\\ETL9B_4",
              "data\\ETL9B\\ETL9B_5"]
ETL1_PATHS = ["data\\ETL1C\\ETL1C_07",
              "data\\ETL1C\\ETL1C_08",
              "data\\ETL1C\\ETL1C_09",
              "data\\ETL1C\\ETL1C_10",
              "data\\ETL1C\\ETL1C_11",
              "data\\ETL1C\\ETL1C_12",
              "data\\ETL1C\\ETL1C_13",]

CURRENT_RUN = 4 #Done except 5
CURRENT_ETL9_PATH = ETL9_PATHS[CURRENT_RUN]

NUM_RECORDS_PER_CHAR = 200

GENERATE = True

if GENERATE:
    process_9B_image = get_simple_image_processer(IMAGE_SIZE, inverted=False)
    process_1C_image = get_kata_image_processor(IMAGE_SIZE, inverted=False)

    # Load hiragana and kanji
    # 40 records per character per file
    # Only enough memory for one file at a time
    x, y = load_data(CURRENT_ETL9_PATH, Record9B, process_image=process_9B_image)
    # x, y = np.empty((0, 64, 64, 1)), np.empty((0,)) # For testing kata only

    # Load katakana
    # 1411 records per character per file
    # 8 characters per file
    # all records for each characters are bundled together
    # meaning records 0 to 1410 are A, 1411 to 2821 are B, etc ...
    # We want 40 records per char so we load a bit of each file
    record_range = []
    # We load the 40 first records out of 1411 for each character.
    # On subsequent runs, as we load new kanji and hiragana from the other ETL9 files
    # We increase the current run offset to load a new set of 40 records for each char
    for i in range(8): record_range += list(range(1411*i + NUM_RECORDS_PER_CHAR*CURRENT_RUN, 1411*i + NUM_RECORDS_PER_CHAR*(CURRENT_RUN+1)))
    for path in ETL1_PATHS:
        if path == ETL1_PATHS[-1]: curr_record_range = record_range[:NUM_RECORDS_PER_CHAR*3] # Only 3 characters in last file
        else: curr_record_range = record_range # 8 characters in other files

        # print(path)

        nx, ny = load_data(path, Record1C, record_range=curr_record_range, process_image=process_1C_image)
        ny = np.apply_along_axis(lambda x: JIS_201_to_208(x[0]), 0, [ny])

        x = np.concatenate((x, nx))
        y = np.concatenate((y, ny))


    uniques = np.load("uniques3084_bu.npy")
    y, uniques = jis_code_to_categorical(y, uniques)
    # np.save("uniques3084.npy", uniques)

    print("Shuffling data.")
    x_shuffled, y_shuffled = sklearn.utils.shuffle(x, y, random_state=0)
    del x
    del y

    np.save("x_shuffled.npy", x_shuffled)
    np.save("y_shuffled.npy", y_shuffled)
else:
    print("Loading shuffled.")
    x_shuffled = np.load("x_shuffled.npy")
    y_shuffled = np.load("y_shuffled.npy")


# Compile or load model
print("Compiling model.")
# You might think 3036 kanji/hira + 51 kata = 3087 but actually it's 3084.
# Not sure why, maybe katakana redundant with kanji or hiragana
# weird stuff, don't really care to take the time to find out
#model = M7_2(n_output=3084, input_shape=(64, 64, 1))
model = load_model("CNN_FULL_M7_2.09-0.979-0.069.h5")
#model = alphabet_classifier("CNN_K_M7_2.21-0.987-0.041.h5")

print("Splitting train and test data.")
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x_shuffled, y_shuffled, test_size=TEST_SPLIT_PERCENTAGE, random_state=42)
del x_shuffled
del y_shuffled

def get_save_callback():
        model_name = "CNN_FULL_M7_2.{epoch:02d}-{acc:.3f}-{loss:.3f}.h5"
        return ModelCheckpoint(model_name, monitor='acc', verbose=1, save_best_only=False)


print("Training model.")
model.fit(x_train, y_train,
          epochs=NUM_EPOCHS,
          batch_size=BATCH_SIZE,
          callbacks= [get_save_callback()])


print("Evaluating model.")
score, acc = model.evaluate(x_test, y_test,
                            batch_size=BATCH_SIZE,
                            verbose=0)

print( "Training size: ", x_train.shape[0])
print( "Test size: ", x_test.shape[0])
print( "Test Score: ", score)
print( "Test Accuracy: ", acc)
