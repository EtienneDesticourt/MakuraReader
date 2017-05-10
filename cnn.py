from keras.models import Sequential
from keras.models import load_model
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import AveragePooling2D
from keras.layers import Activation
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Dense
from keras.optimizers import SGD


class KanjiRecognizer(object):

    def __init__(self, output_size, image_size, learning_rate, epochs):
        self.image_size = image_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.output_size = output_size

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


        model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.output_size))
        model.add(Activation('softmax'))

        optimizer = SGD(lr=self.learning_rate, momentum=0.9, decay=1e-6, nesterov=True)
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
        model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        self.model = model
        model.summary()
        input()

