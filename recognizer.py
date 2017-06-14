from PIL import Image
from keras.models import load_model
import numpy as np
import tensorflow as tf

class Recognizer(object):
    HIRAGANA = 0
    KATAKANA = 1
    KANJI    = 2

    def __init__(self, discriminator_model, kanji_hira_model, kata_model, kanji_labels_file, kata_labels_file,
        image_size=(64, 64), background=(0, 0, 0), threshold=150):
        self.image_size = image_size
        self.background = background
        self.threshold = threshold
        self.discriminator = load_model(discriminator_model)
        self.kanji_model = load_model(kanji_hira_model)
        self.katakana_model = load_model(kata_model)
        self.kanji_labels = np.load(kanji_labels_file)
        self.kata_labels = np.load(kata_labels_file)
        self.graph = tf.get_default_graph()

    def predict_alphabet(self, image):
        alphabet_pred = self.discriminator.predict(image)
        alphabet = np.argmax(alphabet_pred)
        return alphabet

    def predict(self, image):
        alphabet = self.predict_alphabet(image)
        if alphabet == self.HIRAGANA or alphabet == self.KANJI:
            model = self.kanji_model
            other_model = self.katakana_model
            other_alphabet = self.KATAKANA
        else:
            model = self.katakana_model
            other_model = self.kanji_model
            other_alphabet = self.HIRAGANA

        pred = model.predict(image)
        best_match = np.max(pred)

        if best_match < 50:
            new_pred = other_model.predict(image)
            if np.max(new_pred) > best_match:
                return (other_alphabet, new_pred)

        return (alphabet, pred)

    def get_label(self, prediction_vector, alphabet):
        if alphabet == self.KATAKANA:
            return self.kata_labels[prediction_vector.argmax(1)[0]]
        else:
            return self.kanji_labels[prediction_vector.argmax(1)[0]]

    def is_punctuation(self, image):
        w, h = image.size
        colors = image.getcolors(w*h)

        total = 0
        for count, color in colors:
            total += count

        for count, color in colors:
            if color == self.background and count/total > 0.95:
                return True
        return False

    def smart_resize(self, segment_image, background_image):
        result = background_image.copy()
        # Crop black borders
        cropped = segment_image.crop(segment_image.getbbox())
        # Resize to closest 64x64 size while keeping aspect ratio
        target_w, target_h = self.image_size
        w, h = cropped.size
        bigger_side = max(cropped.size)
        nw, nh = target_w * w // bigger_side, target_h * h // bigger_side
        resized = cropped.resize((nw, nh), Image.ANTIALIAS)
        # Paste on center of 64x64 background
        offset = ((target_w - nw) // 2, (target_h - nh) // 2)
        result.paste(resized, offset)
        return result

    def image_to_array(self, image):
        image = image.convert('L')
        image_array = np.array(image)
        image_array = np.where(image_array > self.threshold, 0, 1)
        return image_array[:, :, np.newaxis] #64x64x1

    def jis0208_to_unicode(self, jis_code):
        b = b'\033$B' + bytes.fromhex(hex(jis_code)[2:])
        return b.decode('iso2022_jp')

    def classify(self, characters):
        background = Image.new("RGB", self.image_size, self.background)
        full_text = ""
        for character in characters:
            if not self.is_punctuation(character.segment.image):
                char_image = self.smart_resize(character.segment.image, background)
                image_array = self.image_to_array(char_image)[np.newaxis, :, :, :] #New axis is samples dimension
                with self.graph.as_default():
                    alphabet, char_pred = self.predict(image_array)
                char_jis_code = self.get_label(char_pred, alphabet)
                full_text += self.jis0208_to_unicode(char_jis_code)
            else:
                full_text += ","
            
        return full_text