from keras.models import Sequential
from keras.models import load_model
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import AveragePooling2D
from keras.layers import Activation
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Dense
from keras.optimizers import SGD, Adam
from keras import initializers
from keras.initializers import Constant

class KanjiRecognizer(object):

    def __init__(self, output_size, image_size, learning_rate, epochs):
        self.image_size = image_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.output_size = output_size

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(64, (3, 3), padding="same", input_shape=(self.image_size, self.image_size, 1), kernel_initializer=initializers.VarianceScaling(scale=0.1), bias_initializer=Constant(0.1)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, (3, 3), padding="same", kernel_initializer=initializers.VarianceScaling(scale=0.1),bias_initializer=Constant(0.1) ))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(192, (3, 3), padding="same", kernel_initializer=initializers.VarianceScaling(scale=0.1),bias_initializer=Constant(0.1) ))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(256, (3, 3), padding="same", kernel_initializer=initializers.VarianceScaling(scale=0.1),bias_initializer=Constant(0.1) ))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        model.add(Dense(1024, kernel_initializer=initializers.VarianceScaling(scale=0.1),bias_initializer=Constant(0.1) ))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1024, kernel_initializer=initializers.VarianceScaling(scale=0.1),bias_initializer=Constant(0.1) ))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.output_size))
        model.add(Activation('softmax'))

        optimizer = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.005)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model = model
        model.summary()
        input()
        
    def load_model(self, weights_path):
        self.model = load_model(weights_path)

    def fit(self, train_data, val_data, nb_train_samples, nb_val_samples, callbacks, class_weights=None):
        return self.model.fit_generator(
            train_data,
            samples_per_epoch=nb_train_samples,
            nb_epoch=self.epochs,
            validation_data=val_data,
            nb_val_samples=nb_val_samples,
            callbacks=callbacks,
            class_weight=class_weights)

    def predict(self, sample):
        return self.model.predict(sample)

    def predict_generator(self, test_data, nb_test_samples):
        return self.model.predict_generator(test_data, nb_test_samples)
        
class ElementClassifier(object):

    def __init__(self, output_size, image_size, learning_rate, epochs):
        self.image_size = image_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.output_size = output_size

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(64, (3, 3), padding="same", input_shape=(self.image_size, self.image_size, 1), kernel_initializer=initializers.VarianceScaling(scale=0.1), bias_initializer=Constant(0.1)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, (3, 3), padding="same", kernel_initializer=initializers.VarianceScaling(scale=0.1), bias_initializer=Constant(0.1)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(192, (3, 3), padding="same", kernel_initializer=initializers.VarianceScaling(scale=0.1), bias_initializer=Constant(0.1)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(256, (3, 3), padding="same", kernel_initializer=initializers.VarianceScaling(scale=0.1), bias_initializer=Constant(0.1)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        model.add(Dense(1024, kernel_initializer=initializers.VarianceScaling(scale=0.1), bias_initializer=Constant(0.1)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(1024, kernel_initializer=initializers.VarianceScaling(scale=0.1), bias_initializer=Constant(0.1)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.output_size))
        model.add(Activation('sigmoid'))

        optimizer = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.005)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model = model
        model.summary()
        input()
        
    def load_model(self, weights_path):
        self.model = load_model(weights_path)

    def fit(self, train_data, val_data, nb_train_samples, nb_val_samples, callbacks, class_weights=None):
        return self.model.fit_generator(
            train_data,
            samples_per_epoch=nb_train_samples,
            nb_epoch=self.epochs,
            validation_data=val_data,
            nb_val_samples=nb_val_samples,
            callbacks=callbacks,
            class_weight=class_weights)

    def predict(self, sample):
        return self.model.predict(sample)

    def predict_generator(self, test_data, nb_test_samples):
        return self.model.predict_generator(test_data, nb_test_samples)


class ElementRecognizer(KanjiRecognizer):

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=(self.image_size, self.image_size, 3)))
        model.add(Activation('relu'))
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(Conv2D(64, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))


        model.add(Flatten()) 
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.output_size))
        model.add(Activation('sigmoid'))

        optimizer = SGD(lr=self.learning_rate, momentum=0.9, decay=1e-6, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model = model
        model.summary()
        input()

import os
from keras.applications.inception_v3 import InceptionV3
from keras.layers import Flatten, Dense, AveragePooling2D
from keras.models import Model
from keras.optimizers import SGD
from keras.models import load_model
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"

class InceptionV3Model(object):

    def __init__(self, output_size, image_size, learning_rate, epochs):
        self.image_size = image_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.output_size = output_size

    def reset(self):
        self.model.set_weights(self.init_weights)

    def build_model(self):

        print('Loading InceptionV3 Weights ...')
        InceptionV3_notop = InceptionV3(include_top=False, weights='imagenet',
                                        input_tensor=None, input_shape=(150, 150, 3))

        print('Adding Average Pooling Layer and Softmax Output Layer ...')
        output = InceptionV3_notop.get_layer(index=-1).output  # Shape: (8, 8, 2048)
        output = AveragePooling2D((3, 3), strides=(3, 3), name='avg_pool')(output)
        output = Flatten(name='flatten')(output)
        output = Dense(self.output_size, activation='sigmoid', name='predictions')(output)

        self.model = Model(InceptionV3_notop.input, output)

        optimizer = SGD(lr=self.learning_rate, momentum=0.9, decay=0.0, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.init_weights = self.model.get_weights()

    def load_model(self, weights_path):
        self.model = load_model(weights_path)

    def fit(self, train_data, val_data, nb_train_samples, nb_val_samples, callbacks):
        return self.model.fit_generator(
            train_data,
            samples_per_epoch=nb_train_samples,
            nb_epoch=self.epochs,
            validation_data=val_data,
            nb_val_samples=nb_val_samples,
            callbacks=callbacks)

    def predict(self, test_data, nb_test_samples):
        return self.model.predict_generator(test_data, nb_test_samples)

