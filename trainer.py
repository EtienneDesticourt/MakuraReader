import os
import sklearn.utils
import sklearn.model_selection
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
import numpy as np

from utils.ectl_loader import load_data
from utils.misc import jis_code_to_alphabet, get_simple_image_processer, JIS_201_to_208
from utils.record_9B import Record9B
from utils.record_1C import Record1C
from models.cnn_classifiers import M7_2, alphabet_classifier


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" # Disable warnings
DATASET_PATH = "data\\ETL9B\\ETL9B_1"
TEST_SPLIT_PERCENTAGE = 0.2
NUM_CLASSES = 3
NUM_EPOCHS = 25
BATCH_SIZE = 32
IMAGE_SIZE = (64, 64)

FILE_PATHS = ["data\\ETL9B\\ETL9B_1",
		      "data\\ETL9B\\ETL9B_2",
		      "data\\ETL9B\\ETL9B_3",
		      "data\\ETL9B\\ETL9B_4",
		      "data\\ETL9B\\ETL9B_5",
		      "data\\ETL1C\\ETL1C_07",
			  "data\\ETL1C\\ETL1C_08",
			  "data\\ETL1C\\ETL1C_09",
			  "data\\ETL1C\\ETL1C_10",
			  "data\\ETL1C\\ETL1C_11",
			  "data\\ETL1C\\ETL1C_12",
			  "data\\ETL1C\\ETL1C_13",] # Keep 5th for testing


print("Compiling model.")
model = M7_2(n_output=3, input_shape=(64, 64, 1))
#model = load_model("CNN_K_M7_2_A.06-0.828-2.769.h5")
#model = alphabet_classifier("CNN_K_M7_2.21-0.987-0.041.h5")

x = np.empty((0, 64, 64, 1))
y = np.empty((0, 3))
process_image = get_simple_image_processer(IMAGE_SIZE, inverted=True)
kata_x = np.empty((0, 64, 64, 1))
kata_y = np.empty((0, 3))

SAMPLES_PER_CLASS = 14200

for i in range(len(FILE_PATHS)):
	path = FILE_PATHS[i]
	if "ETL1C" in path: Record = Record1C
	else: Record = Record9B

	print("Loading ECTL data for file:", path)

	nx, ny = load_data(path, Record, process_image=process_image)
	if Record == Record1C:
		ny = np.apply_along_axis(lambda x: JIS_201_to_208(x[0]), 0, [ny])
	ny = jis_code_to_alphabet(ny)


	# Keep only hiragana
	if i in range(5):
		hira_x = nx[np.where(np.all(ny == [1, 0, 0], axis=1))]
		hira_y = ny[np.where(np.all(ny == [1, 0, 0], axis=1))]

		if i == 0: # Load 14200 kanjis from first file (since there are 14200 total hiragana pictures, for balance)
			random_rows = np.random.choice(nx.shape[0], SAMPLES_PER_CLASS, replace=False)
			nx = np.concatenate((nx[random_rows, :, :, :], hira_x))
			ny = np.concatenate((ny[random_rows, :], hira_y))
		else:
			nx = hira_x
			ny = hira_y
		print(nx.shape)
		print(ny.shape)


		x = np.concatenate((x, nx))
		y = np.concatenate((y, ny))

	else:
		kata_x = np.concatenate((kata_x, nx))
		kata_y = np.concatenate((kata_y, ny))

# Keep only 14200 katakanas for balance
random_rows = np.random.choice(kata_x.shape[0], SAMPLES_PER_CLASS, replace=False)
x = np.concatenate((kata_x[random_rows, :, :, :], x))
y = np.concatenate((kata_y[random_rows, :], y))



 

print("Shuffling data.")
x_shuffled, y_shuffled = sklearn.utils.shuffle(x, y, random_state=0)
del x
del y

np.save("x_shuffled.npy", x_shuffled)
np.save("y_shuffled.npy", y_shuffled)

print("Splitting train and test data.")
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x_shuffled, y_shuffled, test_size=TEST_SPLIT_PERCENTAGE, random_state=42)
del x_shuffled
del y_shuffled

def get_save_callback():
        model_name = "CNN_K_M7_2_A.{epoch:02d}-{acc:.3f}-{loss:.3f}.h5"
        return ModelCheckpoint(model_name, monitor='acc', verbose=1, save_best_only=False)


print("Training model.")
model.fit(x_train, y_train,
          epochs=NUM_EPOCHS,
          batch_size=BATCH_SIZE,
          callbacks= [get_save_callback()])


save_model_weights('weights/M7_2_A-kanji_weights.h5', model)

print("Evaluating model.")
score, acc = model.evaluate(x_test, y_test,
                            batch_size=BATCH_SIZE,
                            verbose=0)

print( "Training size: ", x_train.shape[0])
print( "Test size: ", x_test.shape[0])
print( "Test Score: ", score)
print( "Test Accuracy: ", acc)
