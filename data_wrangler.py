import os
import numpy as np
import scipy
from keras.preprocessing.image import ImageDataGenerator
import config

class DataWrangler(object):

    def __init__(self, image_size=config.IMAGE_SIZE, batch_size=config.BATCH_SIZE, train_path=config.TRAIN_DIR, val_path=config.VAL_DIR):
        self.train_path = train_path
        self.val_path = val_path
        self.num_train_samples = len(os.listdir(self.train_path))
        self.num_val_samples = len(os.listdir(self.val_path))
        self.image_size = image_size
        self.batch_size = batch_size

    def get_train_generator(self):
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            shear_range=0.1,
            zoom_range=0.2,
            rotation_range=10.,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=False)
        train_generator = train_datagen.flow_from_directory(self.train_path,
            target_size = self.image_size,
            batch_size = self.batch_size,
            color_mode="grayscale",
            classes = os.listdir(self.train_path))
        return train_generator

    def get_val_generator(self):
        val_datagen = ImageDataGenerator(rescale=1./255)
        validation_generator = val_datagen.flow_from_directory(self.val_path,
            target_size=self.image_size,
            batch_size=self.batch_size,
            color_mode="grayscale",
            classes = os.listdir(self.train_path))
        return validation_generator


class CustomDataWrangler(DataWrangler):

    def get_train_generator(self):
        with open("training.csv") as f: #clean
            data = f.read().split("\n")
        files = []
        data.pop()
        for line in data:
            file_name, label = line.split("\t")
            label_array = np.fromstring(label[1:-1], dtype=int, sep=",")
            file_path = os.path.join(self.train_path, file_name)
            files.append((file_path, label_array))

        class Gen():
            def __init__(gen):
                gen.i = range(0, len(files), self.batch_size)
                gen.j = 0

            def __len__(gen):
                return 2

            def __iter__(gen):
                return gen

            def __next__(gen):
                i = gen.i[gen.j]
                images = np.zeros((self.batch_size, self.image_size[0], self.image_size[1], 1))
                labels = np.zeros((self.batch_size, 128)) #clean
                j = 0
                for path, label in files[i:i+self.batch_size]:
                    image = scipy.misc.imread(path, mode='L')
                    image = image.reshape((self.image_size[0], self.image_size[1], 1))
                    images[j] = image
                    labels[j] = label
                    j += 1
                    
                gen.j += 1
                if gen.j >= len(gen.i):
                    gen.j = 0
                return images, labels

        return Gen()

    def get_val_generator(self):
        with open("validation.csv") as f: #clean
            data = f.read().split("\n")
        data.pop()
        files = []
        for line in data:
            file_name, label = line.split("\t")
            label_array = np.fromstring(label[1:-1], dtype=int, sep=",")
            file_path = os.path.join(self.val_path, file_name)
            files.append((file_path, label_array))

        class Gen():
            def __init__(gen):
                gen.i = range(0, len(files), self.batch_size)
                gen.j = 0

            def __len__(gen):
                return 2

            def __iter__(gen):
                return gen

            def __next__(gen):
                i = gen.i[gen.j]
                images = np.zeros((self.batch_size, self.image_size[0], self.image_size[1], 1))
                labels = np.zeros((self.batch_size, 128)) #clean
                j = 0
                for path, label in files[i:i+self.batch_size]:
                    image = scipy.misc.imread(path, mode='L')
                    image = image.reshape((self.image_size[0], self.image_size[1], 1))
                    images[j] = image
                    labels[j] = label
                    j += 1

                gen.j += 1
                if gen.j >= len(gen.i):
                    gen.j = 0
                return images, labels

        return Gen()
