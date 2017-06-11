from keras.layers import Activation
from keras.layers import AveragePooling2D
from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import MaxPooling2D
from keras.models import Sequential
from keras.models import Model
from keras import initializers
from keras.optimizers import SGD, Adam
from keras.models import load_model


vs_init = initializers.VarianceScaling(scale=0.1)
bias_init = initializers.Constant(0.1)

def M7_2(weights_path=None, input_shape=(64, 64, 1), n_output=None):
    model = Sequential()

    model.add(Conv2D(64, (3, 3), input_shape=input_shape, padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(192, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(256, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1024))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(n_output))
    model.add(Activation('softmax'))

    optimizer = Adam(lr=1e-4)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model


def M7_2_truncated(weights_path):
    model = load_model(weights_path)
    model.pop()
    model.pop()
    return model


def alphabet_classifier(M7_2_weights_path):
    M7_2 = M7_2_truncated(M7_2_weights_path)
    output = M7_2.layers[-1].output
    output = Dense(3, name='last_dense')(output)
    output = Activation('softmax', name='predictions')(output)

    model = Model(M7_2.input, output)
    optimizer = Adam(lr=1e-4)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model











