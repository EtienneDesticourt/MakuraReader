from PIL import Image
from keras.models import load_model
import numpy as np

class Recognizer(object):

    def __init__(self, weights_file, labels_file, image_size=(64, 64), background=(0, 0, 0), threshold=150):
        self.image_size = image_size
        self.background = background
        self.threshold = threshold
        self.model = load_model(weights_file)
        self.labels = np.load(labels_file)

    def predict(self, image):
        return self.model.predict(image)

    def get_label(self, prediction_vector):
        return self.labels[prediction_vector.argmax(1)[0]]

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
        image_array = np.where(image_array > self.threshold, 1, 0)
        return image_array[:, :, np.newaxis] #64x64x1

    def jis0208_to_unicode(self, jis_code):
        b = b'\033$B' + bytes.fromhex(hex(jis_code)[2:])
        return b.decode('iso2022_jp')

    def classify(self, characters):
        background = Image.new("RGB", self.image_size, self.background)
        full_text = ""
        for character in characters:
            char_image = self.smart_resize(character.segment.image, background)
            image_array = self.image_to_array(char_image)[np.newaxis, :, :, :] #New axis is samples dimension
            char_pred = self.predict(image_array)
            char_jis_code = self.get_label(char_pred)
            full_text += self.jis0208_to_unicode(char_jis_code)
            
        return full_text