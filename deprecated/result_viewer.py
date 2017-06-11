import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from cnn import ElementClassifier
import os
import config
import random
import scipy


DATA_DIR = "C:\\DatasetCache\\element_antialias_wb_modern_balanced_nobold\\val"
ELEMENTS_DIR = "C:\\DatasetCache\\elements"
files = os.listdir(DATA_DIR)
file_index = 0


cnn = ElementClassifier(config.NUM_CLASSES, config.IMAGE_SIZE[0], config.LEARNING_RATE, config.EPOCHS)
cnn.load_model(config.MODEL_TO_LOAD)

def predict(path):
    image = scipy.misc.imread(path, mode='L')
    image = image.reshape((64, 64, 1))
    image = image[np.newaxis, :, :, :]
    pred = cnn.predict(image)[0]
    print(pred[pred.argsort()[-10:]])
    return pred.argsort()[-4:] # returns best 4 indexes

fig = plt.figure(figsize=(14,6))

def draw_kanji_class(kanji, elements):	
	fig.add_subplot(1,2,1)
	img = mpimg.imread(kanji)
	plt.imshow(img)

	fig.add_subplot(2,4,3)
	img = mpimg.imread(elements[0])
	plt.imshow(img)

	fig.add_subplot(2,4,4)
	img = mpimg.imread(elements[1])
	plt.imshow(img)

	fig.add_subplot(2,4,7)
	img = mpimg.imread(elements[2])
	plt.imshow(img)

	fig.add_subplot(2,4,8)
	img = mpimg.imread(elements[3])
	plt.imshow(img)

def onclick(event):
	file_name = random.choice(files)
	kanji = os.path.join(DATA_DIR, file_name)
	elements = []
	for element in predict(kanji):
		file_name = os.path.join(ELEMENTS_DIR, str(element) + ".jpg")
		elements.append(file_name)
	print(elements[-1])

	fig.clf()
	draw_kanji_class(kanji, elements)

	fig.canvas.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()