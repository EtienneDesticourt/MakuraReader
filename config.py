
recognizer_config = {
    "model_path": r"tests\data\model.h5",
    "labels_path": r"tests\data\labels.npy",
    "background_color": (0, 0, 0),
    "threshold": 150
}

history_config = {
    "path": r"data\makura.hist"
}



TARGET = "kindle"
L_THRESHOLD = 150
MODEL_PATH = "weights\\CNN_FULL_M7_2_FULL.16-0.956-0.144.h5"#"weights\\CNN_FULL_M7_2.09-0.979-0.069.h5"
LABELS_PATH = "weights\\uniques3151.npy"#"weights\\labels_full.npy"
DIC_PATH = "data\\JMdict_e"
DIC_DATABASE = "data\\jdict.sqlite"
RENDERING_FONT_FILE = 'msgothic.ttc' #'msmincho.ttc'
RENDERING_FONT_SIZE = 17
LINE_WIDTH = 45
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
KINDLE_BBOX = (212, 155, 655, 960)
KINDLE_LINE_WIDTH = 45
KINDLE_CHAR_MIN_SIZE = 26
KINDLE_CHAR_MAX_SIZE = 32
KINDLE_TOO_BIG_RECTIFIER = 10
PAGE_CHANGE_THRESHOLD = 1
BOX_SIZE = (443, 805)
BOTTOM_MARGIN = 0.1
SPREAD_RATIO = 1.2
DATA_DIR = "data"
LOAD_FROM_MODEL = False
MODEL_TO_LOAD = "models\\elements_128_wb_balanced\\CNN_ELEMENTS_TRUNC_M7.00-0.099-13.968-0.101-14.973.h5"
VAL_DIR = "C:\\DatasetCache\\element_antialias_wb_modern_balanced_nobold\\val"
TRAIN_DIR = "C:\\DatasetCache\\element_antialias_wb_modern_balanced_nobold\\train"
HD_TRAIN_DIR = "hd_data\\train"
HD_VAL_DIR = "hd_data\\val"
KANJI_LIST = "kanji.txt"
FONT_DIR = "C:\\Windows\\Fonts"
FONT_GOTHIC = "msgothic.ttc"
FONT_ARIAL = "ARIALUNI.TTF"
TRAINING_PERCENT = 0.8
FONTS = ['AdobeHeitiStd-Regular.otf',
         'AdobeSongStd-Light.otf',
         'ARIALUNI.TTF',
         'irohamaru-mikami-Regular.ttf',
         'KozGoPr6N-Bold.otf',
         'KozGoPr6N-ExtraLight.otf',
         'KozGoPr6N-Heavy.otf',
         'KozGoPr6N-Light.otf',
         'KozGoPr6N-Medium.otf',
         'KozGoPr6N-Regular.otf',
         'KozGoPro-Bold.otf',
         'KozGoPro-ExtraLight.otf',
         'KozGoPro-Heavy.otf',
         'KozGoPro-Light.otf',
         'KozGoPro-Medium.otf',
         'KozGoPro-Regular.otf',
         'KozMinPr6N-Bold.otf',
         'KozMinPr6N-ExtraLight.otf',
         'KozMinPr6N-Heavy.otf',
         'KozMinPr6N-Light.otf',
         'KozMinPr6N-Medium.otf',
         'KozMinPr6N-Regular.otf',
         'KozMinPro-Bold.otf',
         'KozMinPro-ExtraLight.otf',
         'KozMinPro-Heavy.otf',
         'KozMinPro-Light.otf',
         'msmincho.ttc',
         'msgothic.ttc',
         'KozMinPro-Medium.otf',
         'KozMinPro-Regular.otf',
         'meiryo.ttc',
         'meiryob.ttc',
         'simhei.ttf',
         'simsun.ttc']
FONTS = ['AdobeHeitiStd-Regular.otf',
         'AdobeSongStd-Light.otf',
         'ARIALUNI.TTF',
         'irohamaru-mikami-Regular.ttf',
         'KozGoPr6N-ExtraLight.otf',
         'KozMinPr6N-Light.otf',
         'KozGoPro-Light.otf',
         'msmincho.ttc',
         'KozMinPr6N-Regular.otf',
         'msgothic.ttc']
# VAL_FONTS = ['msgothic.ttc',
#            'KozMinPro-Medium.otf',
#            'KozMinPro-Regular.otf',
#            'meiryo.ttc',
#            'meiryob.ttc',
#            'simhei.ttf',
#            'simsun.ttc']
FONT_SIZE = 40
FONT_SIZES = [25, 26, 27]#[16, 20, 24, 28, 30]
COLOR = (255, 255, 255)
TEXT_OFFSET = (10, 10)
IMAGE_SIZE = (64, 64)
BACKGROUND = (0, 0, 0)
LEARNING_RATE = 0.1
BATCH_SIZE = 64
NUM_AUGMENTATIONS = 1
EPOCHS = 250
NUM_CLASSES = 128

#Ensemble cut last layer of kanji cnn, fuse second to last with last layer of element cnn and feed to FC dense layer with 2500 outputs