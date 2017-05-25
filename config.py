DATA_DIR = "data"
VAL_DIR = "data\\val"
TRAIN_DIR = "data\\train"
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
# FONTS = ['AdobeHeitiStd-Regular.otf',
# 		 'AdobeSongStd-Light.otf',
# 		 'ARIALUNI.TTF',
# 		 'irohamaru-mikami-Regular.ttf',
# 		 'KozGoPr6N-ExtraLight.otf',
# 		 'KozMinPr6N-Light.otf',
# 		 'KozGoPro-Light.otf',
# 		 'msmincho.ttc',
# 		 'KozMinPr6N-Regular.otf',
# 		 'msgothic.ttc']
# VAL_FONTS = ['msgothic.ttc',
# 			 'KozMinPro-Medium.otf',
# 			 'KozMinPro-Regular.otf',
# 			 'meiryo.ttc',
# 			 'meiryob.ttc',
# 			 'simhei.ttf',
# 			 'simsun.ttc']
FONT_SIZE = 40
FONT_SIZES = [24, 26, 28]#[16, 20, 24, 28, 30]
COLOR = (255, 255, 255)
TEXT_OFFSET = (10, 10)
IMAGE_SIZE = (64, 64)
BACKGROUND = (0, 0, 0)
LEARNING_RATE = 0.01
BATCH_SIZE = 32
NUM_AUGMENTATIONS = 1
EPOCHS = 250

#Ensemble cut last layer of kanji cnn, fuse second to last with last layer of element cnn and feed to FC dense layer with 2500 outputs