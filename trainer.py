import os
import sklearn.utils
import sklearn.model_selection
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
import numpy as np

from utils.ectl_loader import load_data
from utils.misc import jis_code_to_alphabet, get_simple_image_processer, JIS_201_to_208, jis_code_to_categorical, get_kata_image_processor
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

FILE_PATHS = ["data\\ETL1C\\ETL1C_07",
			  "data\\ETL1C\\ETL1C_08",
			  "data\\ETL1C\\ETL1C_09",
			  "data\\ETL1C\\ETL1C_10",
			  "data\\ETL1C\\ETL1C_11",
			  "data\\ETL1C\\ETL1C_12",
			  "data\\ETL1C\\ETL1C_13",] # Keep 5th for testing


#model = load_model("CNN_K_M7_2_A.24-0.998-0.006.h5")
#model = alphabet_classifier("CNN_K_M7_2.21-0.987-0.041.h5")

x = np.empty((0, 64, 64, 1))
y = np.empty((0,))
#process_image = get_simple_image_processer(IMAGE_SIZE, inverted=True)
process_image = get_kata_image_processor(IMAGE_SIZE, inverted=True)


for path in FILE_PATHS:

	print("Loading ECTL data for file:", path)

	nx, ny = load_data(path, Record1C, process_image=process_image)
	ny = np.apply_along_axis(lambda jis: JIS_201_to_208(jis[0]), 0, [ny])

	x = np.concatenate((x, nx))
	y = np.concatenate((y, ny))


y, unique_labels = jis_code_to_categorical(y)
np.save("kata_labels.npy", unique_labels)

print("Compiling model.")
print(y.shape[1], "classes.")
model = M7_2(n_output=y.shape[1], input_shape=(64, 64, 1))
 

print("Shuffling data.")
x_shuffled, y_shuffled = sklearn.utils.shuffle(x, y, random_state=0)
del x
del y

np.save("x_shuffled.npy", x_shuffled)
np.save("y_shuffled.npy", y_shuffled)

# x_shuffled = np.load("x_shuffled_kata.npy")
# y_shuffled = np.load("y_shuffled_kata.npy")

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



print("Evaluating model.")
score, acc = model.evaluate(x_test, y_test,
                            batch_size=BATCH_SIZE,
                            verbose=0)

print( "Training size: ", x_train.shape[0])
print( "Test size: ", x_test.shape[0])
print( "Test Score: ", score)
print( "Test Accuracy: ", acc)
