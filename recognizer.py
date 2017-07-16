from PIL import Image
from keras.models import load_model
import numpy as np
import tensorflow as tf
import config
from utils.misc import smart_resize, image_to_array, jis0208_to_unicode, get_color_percentage

class Recognizer(object):
    "An object which applies optical character recognition algorithms to images."

    def __init__(self, background_color=config.BACKGROUND_COLOR,
                       image_size=config.IMAGE_SIZE,
                       model_path=config.MODEL_PATH,
                       labels_path=config.LABELS_PATH,
                       threshold=config.L_THRESHOLD):
        self.model = load_model(model_path)
        self.labels = np.load(labels_path)
        self.graph = tf.get_default_graph() # Necessary to call tf models from threads
        self.background_color = background_color
        self.background = Image.new("RGB", image_size, background_color)
        self.image_size = image_size
        self.threshold = threshold

    def is_punctuation(self, image):
        percent = get_color_percentage(image, self.background_color)
        return percent > 0.95

    def is_blank(self, image):
        w, h = image.size
        colors = image.getcolors(w*h)

        total = 0
        for count, color in colors:
            total += count

        for count, color in colors:
            if color == self.background_color and count/total > 0.99: # TODO: Replace by config thresh
                return True
        return False

    def categorical_to_jis(self, prediction_vector):
        return self.labels[prediction_vector.argmax(1)]

    def process_image(self, image, background):
        image = smart_resize(image, background, self.image_size)
        return image_to_array(image, self.threshold)

    def transcribe(self, characters):
        bg_copy = self.background.copy()

        # Build array out of all the images
        array = np.empty((0, *self.image_size, 1))
        for character in characters:
            image = character.image
            im_array = self.process_image(image, bg_copy)[np.newaxis, :, :, :]
            array = np.concatenate((array, im_array))

        # Predict and transcribe
        with self.graph.as_default():
            labels = self.model.predict(array)
        jis_codes = self.categorical_to_jis(labels)
        chars = [jis0208_to_unicode(code) for code in jis_codes]

        # Repredict punctuation
        point_indexes = [i for i, character in enumerate(characters) if self.is_punctuation(character.image)]
        for i in point_indexes: chars[i] = ","

        for i, character in enumerate(characters):
            character.text = chars[i]

        return characters
