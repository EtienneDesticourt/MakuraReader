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

def image_is_blank(image, background_color=(0, 0, 0), threshold=0.99):
    w, h = image.size
    colors = image.getcolors(w*h)

    total = 0
    for count, color in colors:
        total += count

    for count, color in colors:
        if color == background_color and count/total > threshold:
            return True
    return False


def image_to_array(image, threshold):
    image = image.convert('L')
    image_array = np.array(image)
    image_array = np.where(image_array > threshold, 1, 0)
    return image_array[:, :, np.newaxis]


def jis0208_to_unicode(jis_code):
    b = b'\033$B' + bytes.fromhex(hex(jis_code)[2:])
    return b.decode('iso2022_jp')

def unicode_to_jis208(u):
    b = u.encode('iso2022_jp')
    b = b[3:-3]
    b = b.decode("utf8")
    if b == "": return -1
    return 256*ord(b[0]) + ord(b[1])

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

def is_kanji(character):
    # kanjis don't follow each other in unicode table
    # they do somewhat in jis208 table so we can just check ~60 ranges of jis codes instead of 6000+ kanji values
    jiscode = unicode_to_jis208(character)
    if jiscode == -1: return False
    i = jiscode
    return (i>=12322 and i<=12414) or (i>=12577 and i<=12670) or (i>=12833 and i<=12926) or (i>=13089 and i<=13182) or (i>=13345 and i<=13438) or (i>=13601 and i<=13694) or (i>=13857 and i<=13950) or (i>=14113 and i<=14206) or (i>=14369 and i<=14462) or (i>=14625 and i<=14718) or (i>=14881 and i<=14974) or (i>=15137 and i<=15230) or (i>=15393 and i<=15486) or (i>=15649 and i<=15742) or (i>=15905 and i<=15998) or (i>=16161 and i<=16254) or (i>=16417 and i<=16510) or (i>=16673 and i<=16766) or (i>=16929 and i<=17022) or (i>=17185 and i<=17278) or (i>=17441 and i<=17534) or (i>=17697 and i<=17790) or (i>=17953 and i<=18046) or (i>=18209 and i<=18302) or (i>=18465 and i<=18558) or (i>=18721 and i<=18814) or (i>=18977 and i<=19070) or (i>=19233 and i<=19326) or (i>=19489 and i<=19582) or (i>=19745 and i<=19838) or (i>=20001 and i<=20094) or (i>=20257 and i<=20307) or (i>=20513 and i<=20606) or (i>=20769 and i<=20862) or (i>=21025 and i<=21118) or (i>=21281 and i<=21374) or (i>=21537 and i<=21630) or (i>=21793 and i<=21886) or (i>=22049 and i<=22142) or (i>=22305 and i<=22398) or (i>=22561 and i<=22654) or (i>=22817 and i<=22910) or (i>=23073 and i<=23166) or (i>=23329 and i<=23422) or (i>=23585 and i<=23678) or (i>=23841 and i<=23934) or (i>=24097 and i<=24190) or (i>=24353 and i<=24446) or (i>=24609 and i<=24702) or (i>=24865 and i<=24958) or (i>=25121 and i<=25214) or (i>=25377 and i<=25470) or (i>=25633 and i<=25726) or (i>=25889 and i<=25982) or (i>=26145 and i<=26238) or (i>=26401 and i<=26494) or (i>=26657 and i<=26750) or (i>=26913 and i<=27006) or (i>=27169 and i<=27262) or (i>=27425 and i<=27518) or (i>=27681 and i<=27774) or (i>=27937 and i<=28030) or (i>=28193 and i<=28286) or (i>=28449 and i<=28542) or (i>=28705 and i<=28798) or (i>=28961 and i<=29054) or (i>=29217 and i<=29310) or (i>=29473 and i<=29566)

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

# for i in range(161, 166):
#     print("\t\t\t %s: %s," % (i, ""))

def JIS_201_to_208(jis_201_code):
    table = {32: 0x2121,
             33: 0x212A,
             34: 0x2148,
             35: 0x2172,
             36: 0x2170,
             37: 0x2173,
             38: 0x2175,
             39: 0x2146,
             40: 0x214A,
             41: 0x214B,
             42: 0x2176,
             43: 0x215C,
             44: 0x2124,
             45: 0x213E,
             46: 0x2125,
             47: 0x2160,
             48: 0x2330,
             49: 0x2331,
             50: 0x2332,
             51: 0x2333,
             52: 0x2334,
             53: 0x2335,
             54: 0x2336,
             55: 0x2337,
             56: 0x2338,
             57: 0x2339,
             58: 0x2127,
             59: 0x2128,
             60: 0x2163,
             61: 0x2161,
             62: 0x2164,
             63: 0x2129,
             64: 0x2177,
             65: 0x2341,
             66: 0x2342,
             67: 0x2343,
             68: 0x2344,
             69: 0x2345,
             70: 0x2346,
             71: 0x2347,
             72: 0x2348,
             73: 0x2349,
             74: 0x234a,
             75: 0x234b,
             76: 0x234c,
             77: 0x234d,
             78: 0x234e,
             79: 0x234f,
             80: 0x2350,
             81: 0x2351,
             82: 0x2352,
             83: 0x2353,
             84: 0x2354,
             85: 0x2355,
             86: 0x2356,
             87: 0x2357,
             88: 0x2358,
             89: 0x2359,
             90: 0x235a,
             91: 0x214E,
             92: 0x216F,
             93: 0xFF3D,
             94: 0x2130,
             95: 0x2132,
             96: 0x212E,
             97: 0x2361,
             98: 0x2362,
             99: 0x2363,
             100: 0x2364,
             101: 0x2365,
             102: 0x2366,
             103: 0x2367,
             104: 0x2368,
             105: 0x2369,
             106: 0x236a,
             107: 0x236b,
             108: 0x236c,
             109: 0x236d,
             110: 0x236e,
             111: 0x236f,
             112: 0x2370,
             113: 0x2371,
             114: 0x2372,
             115: 0x2373,
             116: 0x2374,
             117: 0x2375,
             118: 0x2376,
             119: 0x2377,
             120: 0x2378,
             121: 0x2379,
             122: 0x237a,
             123: 0x2150,
             124: 0x2143,
             125: 0x2151,
             126: 0x2131,
             161: 0x2123,
             162: 0x2156,
             163: 0x2157,
             164: 0x2122,
             165: 0x2126,
             166: 0x2572,
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
             221: 0x2573,
             222: 0x212B,
             223: 0x212C,}
    return table[jis_201_code]