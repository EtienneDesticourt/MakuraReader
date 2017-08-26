from keras.models import load_model
import numpy as np
import tensorflow as tf
from PIL import Image
from utils.misc import smart_resize
from utils.misc import image_to_array
from utils.misc import jis0208_to_unicode
from utils.misc import get_color_percentage


class Recognizer(object):
    """Transforms images into text.

    Uses a model that takes as input an array of shape 
    (num_samples, img_width, img_height, img_channels) and returns
    an array of shape (num_samples, num_characters) with num_characters
    being the length of the character set the model was trained on.
    The model returns a list of softmax probabilities that each character
    appears in a specific image. The list returned is ordered according
    to an array of labels stored alongside the modeled so that the
    indices of probabilities in the list match the indices of the
    labels.

    For example the model might return:
    >> [0.1 0.0 0.7 0.2]
    For the following array of labels:
    >> ["A", "B", "C", "D"]
    In which case the detected character would be "C".

    # Arguments
        model_path: The path to the h5 file containing the model's weights.
        labels_path: The ordered list of labels that match the label indices
                     returned by the model
        background_color: The background color of the images the model
                          has learned to recognize.
        threshold: The threshold at which a pixel is considered to be white.
    """

    def __init__(self, model_path, labels_path, background_color, threshold):
        self.model = load_model(model_path)
        self.ordered_jis_codes = np.load(labels_path)
        # Input shape is (num_samples, width, height, channels)
        self.image_size = self.model.layers[0].input_shape[1:3]
        self.background_color = background_color
        self.background = Image.new("RGB",
                                    self.image_size,
                                    self.background_color)
        self.threshold = threshold
        # Tensorflow only works in main thread, TODO: get rid of tf
        self.main_thread_graph = tf.get_default_graph()

    def _to_array(self, image):
        image = smart_resize(image, self.background, self.image_size)
        return image_to_array(image, self.threshold)

    def _predict(self, image_array):
        # Tensorflow only works in main thread, TODO: get rid of tf
        with self.main_thread_graph.as_default():
            labels = self.model.predict(image_array)

        indices = np.argmax(labels, axis=1)
        jis_codes = self.ordered_jis_codes[indices]
        characters = [jis0208_to_unicode(code) for code in jis_codes]
        text = "".join(characters)

        return text

    def transcribe(self, images):
        """Takes a list of images of characters into a string.

        # Arguments
            images: A list of images of any length and size.

        # Returns
            A string of the characters contained in the images
            with a certain percentage of accuracy.
        """
        if not len(images):
            return ""

        image_array = np.zeros((len(images), *self.image_size, 1))
        for i, image in enumerate(images):
            array = self._to_array(image)
            image_array[i] = array

        text = self._predict(image_array)

        # Temporary punctuation fix until I train a better model
        for i, image in enumerate(images):
            percent = get_color_percentage(image, self.background_color)
            if percent > 0.95:
                text = text[:i] + "," + text[i + 1:]

        return text
