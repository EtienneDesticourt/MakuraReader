
# def reverse_one_hot(labels, unique_classes):
# 	num_classes = len(unique_classes)
# 	argmax(labels, axis=1)

import numpy as np
from keras import np_utils

def jis_code_to_alphabet(labels):
	new_labels = np.zeros((labels.shape[0], 3))
	print(new_labels.shape)
	# Hiragana
	hiragana = np.logical_and(labels >= 0x2421, labels <= 0x2473)
	print(sum(hiragana))
	new_labels[hiragana] = np.array([1, 0, 0])
	# Katakana
	katakana = np.logical_and(labels >= 0x2521, labels <= 0x2576)
	print(sum(katakana))
	new_labels[katakana] = [0, 1, 0]
	# Kanji
	kanji = np.logical_and(np.logical_not(hiragana), np.logical_not(katakana))
	print(sum(kanji))
	new_labels[kanji] = [0, 0, 1]

	return new_labels


def get_simple_image_processer(image_size, inverted=False):	
    background = Image.new('1', image_size)
    def process_image(image):
        background.paste(image) # 64x63 to 64x64
        if inverted:
            new_image = Image.eval(background, lambda x: not x)
        else:
            new_image = background
        return background
    return process_image


def jis_code_to_categorical(labels):	
    unique_labels = list(set(labels))
    labels_dict = {unique_labels[i]: i for i in range(len(unique_labels))}
    new_labels = np.array([labels_dict[l] for l in labels], dtype=np.int32)
    y = np_utils.to_categorical(new_labels, len(unique_labels))
    return y, unique_labels