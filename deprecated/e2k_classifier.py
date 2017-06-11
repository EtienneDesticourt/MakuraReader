from keras.models import Sequential
from keras.models import load_model
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import AveragePooling2D
from keras.layers import Activation
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Input
from keras.optimizers import SGD, Adam
from keras import initializers
from keras.initializers import Constant
from keras.models import Model

class E2KClassifier(object):

    def __init__(self, element_cnn, learning_rate, epochs):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.element_cnn = element_cnn

    def build_model(self):
        element_classifier = load_model(self.element_cnn)
        for layer in element_classifier.layers:
        	layer.trainable = False
        output=element_classifier.get_layer(index=-1).output
        output = Dropout(0.1, name="dropout_7")(output)
        output = Dense(1024, name="dense_4")(output)
        output = Activation('relu', name="activation_8")(output)
        output = Dropout(0.5, name="dropout_8")(output)
        output = Dense(2500, name="dense_5")(output)
        output = Activation('softmax', name="activation_9")(output)


        model = Model(input=element_classifier.input, output=output)

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
        