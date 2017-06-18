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
NUM_EPOCHS = 25
BATCH_SIZE = 64
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

CURRENT_ETL9_PATH = ETL9_PATHS[0]

GENERATE = True

if GENERATE:
	process_9B_image = get_simple_image_processer(IMAGE_SIZE, inverted=True)
	process_1C_image = get_kata_image_processor(IMAGE_SIZE, inverted=True)

	# Load hiragana and kanji
	# 40 records per character per file
	# Only enough memory for one file at a time
	x, y = load_data(CURRENT_ETL9_PATH, Record9B, process_image=process_9B_image, truncate=100)

	# Load katakana
	# 1411 records per character per file
	# 8 characters per file
	# all records for each characters are bundled together
	# meaning records 0 to 1410 are A, 1411 to 2821 are B, etc ...
	# We want 40 records per char so we load a bit of each file
	# You might think 3036 kanji/hira + 51 kata = 3087 but actually it's 3084.
	# Not sure why, maybe katakana redundant with kanji or hiragana
	# weird stuff, don't really care to take the time to find out
	record_range_40 = []
	for i in range(8): record_range_40 += list(range(1411*i, 1411*i+40))
	for path in ETL1_PATHS:
		if path == ETL1_PATHS[-1]: record_range = record_range_40[:40*3] # Only 3 characters in last file
		else: record_range = record_range_40 # 8 characters in other files

		nx, ny = load_data(path, Record1C, record_range=record_range, process_image=process_1C_image)
		ny = np.apply_along_axis(lambda x: JIS_201_to_208(x[0]), 0, [ny])

		x = np.concatenate((x, nx))
		y = np.concatenate((y, ny))


	y, uniques = jis_code_to_categorical(y)
	np.save("uniques3084.npy", uniques)

	print("Shuffling data.")
	x_shuffled, y_shuffled = sklearn.utils.shuffle(x, y, random_state=0)
	del x
	del y

	np.save("x_shuffled.npy", x_shuffled)
	np.save("y_shuffled.npy", y_shuffled)
else:
	x_shuffled = np.load("x_shuffled.npy")
	y_shuffled = np.load("y_shuffled.npy")


# Compile or load model
print("Compiling model.")
model = M7_2(n_output=3084, input_shape=(64, 64, 1))
#model = load_model("CNN_K_M7_2_A.06-0.828-2.769.h5")
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
