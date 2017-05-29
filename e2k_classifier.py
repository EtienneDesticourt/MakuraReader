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

class E2KClassifier(object):

    def __init__(self, learning_rate, epochs):
        self.learning_rate = learning_rate
        self.epochs = epochs

    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_shape=(128,)))
        model.add(Dropout(0.1))
        model.add(Dense(1024))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2500))
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
        