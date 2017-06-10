from keras.utils import np_utils
import numpy as np
import time
from PIL import Image

from utils.record_9B import Record9B
from utils.record_1C import Record1C
from utils.record_generator import RecordGenerator
from utils.misc import kanji_to_alphabet
from utils.simple_verbose_counter import SimpleVerboseCounter

class ECTLLoader(object):

    def __init__(self, num_classes):
        self.num_classes = num_classes

    def load_data(self, file_path, process_image=lambda x: x, truncate=0, alphabet=False):
        count = SimpleVerboseCounter(period=24000, message="Loaded {} total. {} elapsed since last.")

        x = [] #np.empty((0, *Record9B.IMAGE_SIZE[::-1], 1))
        labels = [] #np.array([])
        with open(file_path, "rb") as f:
            for record in RecordGenerator(f, Record9B, num_dummy_records=1):
                image = process_image(record.image)
                image_array = np.asarray(image.getdata()).reshape(image.size)
                x.append(image_array)
                labels.append(record.JIS_code)

                if truncate and count >= truncate: break
                count()

        x = np.asarray(x, dtype=np.uint8)[:, :, :, np.newaxis]
        y = np.asarray(labels, dtype=np.int32)

        return x, y

        # if alphabet:
        #     y = kanji_to_alphabet(labels)
        #     unique_labels = [0, 1, 2]
        # else:
        #     # rename labels from 0 to n_labels-1


        # # Arrange labels
        # unique_labels = list(set(labels)) # Discrete jis codes
        # # Transform jis codes into 0 to num_classes-1 labels for one hot encoding
        # jis_code_to_class = {}
        # for class_number in range(self.num_classes):
        #     jis_code = unique_labels[class_number]
        #     jis_code_to_class[jis_code] = class_number
        # index_labels = np.array([jis_code_to_class[jis_code] for jis_code in labels], dtype=np.int32) 
        # # One hot encode
        # labels = np_utils.to_categorical(index_labels, self.num_classes)

        return x, y, unique_labels
    
    def load_data_1C(self, file_path, image_size=(64, 64), truncate=0, alphabet=False, inverted=True, verbose=False):


        image = Image.new('1', image_size)
        with open(file_path, "rb") as f:
            for record in RecordGenerator(f, Record1C):
                image.paste(record.image.convert('1'))



if __name__ == "__main__":
    from PIL import Image
    with open("data\\ETL9B\\ETL9B_1", "rb") as f:
        for record in RecordGenerator9B(f):        
            print(record.sheet_number, hex(record.JIS_code))
            array = record.image_array
            print(array.shape)
            record.image.show()
            print(record.image.size)
            a = Image.fromarray(array.astype('uint8')*255, mode="L")
            print(a.size)
            a.show()
            #record.image.show()
            input()
