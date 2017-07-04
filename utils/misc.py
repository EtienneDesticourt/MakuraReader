import numpy as np
from keras.utils import np_utils
from PIL import Image, ImageEnhance

def get_color_percentage(image, color):
    w, h = image.size
    colors = image.getcolors(w*h)

    total = sum([count for count, color in colors])
    colors = {color:count for count, color in colors}
    return colors.get(color, 0) / total


def smart_resize(segment_image, background_image, target_size):
    result = background_image.copy()
    # Crop black borders
    cropped = segment_image.crop(segment_image.getbbox())
    # Resize to closest 64x64 size while keeping aspect ratio
    target_w, target_h = target_size
    w, h = cropped.size
    bigger_side = max(cropped.size)
    nw, nh = target_w * w // bigger_side, target_h * h // bigger_side
    resized = cropped.resize((nw, nh), Image.ANTIALIAS)
    # Paste on center of 64x64 background
    offset = ((target_w - nw) // 2, (target_h - nh) // 2)
    result.paste(resized, offset)
    return result


def image_to_array(image, threshold):
    image = image.convert('L')
    image_array = np.array(image)
    image_array = np.where(image_array > threshold, 1, 0)
    return image_array[:, :, np.newaxis]


def jis0208_to_unicode(jis_code):
    b = b'\033$B' + bytes.fromhex(hex(jis_code)[2:])
    return b.decode('iso2022_jp')


def jis_code_to_alphabet(labels):
    new_labels = np.zeros((labels.shape[0], 3))
    print(new_labels.shape)
    # Hiragana
    hiragana = np.logical_and(labels >= 0x2421, labels <= 0x2473)
    print("Hiragana:",sum(hiragana))
    new_labels[hiragana] = np.array([1, 0, 0])
    # Katakana
    katakana = np.logical_and(labels >= 0x2521, labels <= 0x2576)
    print("Katakana:",sum(katakana))
    new_labels[katakana] = [0, 1, 0]
    # Kanji
    kanji = np.logical_and(np.logical_not(hiragana), np.logical_not(katakana))
    print("Kanji:", sum(kanji))
    new_labels[kanji] = [0, 0, 1]

    return new_labels


def get_simple_image_processer(image_size, inverted=False): 
    background = Image.new('1', image_size)
    def process_image(image):
        background.paste(image) # 64x63 to 64x64
        if inverted:
            new_image = Image.eval(background, lambda x: not x)
        else:
            new_image = background
        return new_image
    return process_image


def get_kata_image_processor(image_size, inverted=True):
    background = Image.new('1', image_size)
    def process_image(image):
        image = image.convert('P')
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(40)
        background.paste(image) # 64x63 to 64x64
        if inverted:
            new_image = Image.eval(background, lambda x: not x)
        else:
            new_image = background
        return new_image
    return process_image


def jis_code_to_categorical(labels, unique_labels=None):    
    if type(unique_labels) == type(None):
        unique_labels = list(set(labels))
    labels_dict = {unique_labels[i]: i for i in range(len(unique_labels))}
    new_labels = np.array([labels_dict[l] for l in labels], dtype=np.int32)
    y = np_utils.to_categorical(new_labels, len(unique_labels))
    return y, np.array(unique_labels)


def JIS_201_to_208(jis_201_code):
    table = {166: 0x2572,
             168: 0x2523,
             170: 0x2527,
             177: 0x2522,
             178: 0x2524,
             179: 0x2526,
             180: 0x2528,
             181: 0x2529,
             182: 0x252b,
             183: 0x252d,
             184: 0x252f,
             185: 0x2531,
             186: 0x2533,
             187: 0x2535,
             188: 0x2537,
             189: 0x2539,
             190: 0x253b,
             191: 0x253d,
             192: 0x253f,
             193: 0x2541,
             194: 0x2544,
             195: 0x2546,
             196: 0x2548,
             197: 0x254a,
             198: 0x254b,
             199: 0x254c,
             200: 0x254d,
             201: 0x254e,
             202: 0x254f,
             203: 0x2552,
             204: 0x2555,
             205: 0x2558,
             206: 0x255b,
             207: 0x255e,
             208: 0x255f,
             209: 0x2560,
             210: 0x2561,
             211: 0x2562,
             212: 0x2564,
             213: 0x2566,
             214: 0x2568,
             215: 0x2569,
             216: 0x256A,
             217: 0x256B,
             218: 0x256C,
             219: 0x256D,
             220: 0x256F,
             221: 0x2573,}
    return table[jis_201_code]