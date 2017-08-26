from renderer import Renderer
from kindle_reader import KindleReader
from naive_segmenter import NaiveSegmenter
from collections import namedtuple
from recognizer import Recognizer
from tokenizer import Tokenizer, Token
from history import History
from word import Word
import time
import threading
from ui.token_table_generator import TokenTableGenerator
import sys
import config
import utils.misc
import os
import re

FULL_MODEL = "weights\\CNN_FULL_M7_2.09-0.979-0.069.h5"
FULL_LABELS = "weights\\labels_full.npy"
OUTPUT_PATH = "ui\\images\\generated.png"


Character = namedtuple('Character', ['segment', 'text'])


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class ReaderHelper(object):

    def __init__(self, output_path=OUTPUT_PATH):
        self.reader = KindleReader()
        self.segmenter = NaiveSegmenter()
        self.tokenizer = Tokenizer()
        self.renderer = Renderer()
        self.recognizer = Recognizer(**config.recognizer_config)
        self.history = History(**config.history_config)
        self.history.load()
        self.output_path = output_path
        self.running = True

    def start(self):
        t = threading.Thread(target=self.run)
        t.start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if self.reader.page_has_changed():
                image = self.draw()
            time.sleep(1)

    def draw(self):
        image = self.reader.capture_kindle()
        characters = self.segmenter.get_characters(image)
        characters = [
            c for c in characters if not utils.misc.image_is_blank(c.image)]
        images = [c.image for c in characters]
        text = self.recognizer.transcribe(images)
        for i, character in enumerate(characters):
            character.text = text[i]
        tokens = self.tokenizer.tokenize(characters)
        for token in tokens:
            contexts = re.findall("(?:^|,)(?:(?!,).)*?%s.*?(?:$|,)" % token.raw, text)
            if len(token.english) >= 2:
                kana = token.english[1]
            else:
                kana = token.kana
            if len(token.english) >= 3:
                english = token.english[2]
            else:
                english = ""
            word = Word(token.base, kana, english, contexts)
            self.history.add_word(word)
        tokens = self.renderer.render(tokens)
        tok_gen = TokenTableGenerator()
        tok_gen.generate_index(tokens)
        return image


if __name__ == "__main__":
    # TODO: Remove black characters       X
    # TODO: Fix order                     X
    # TODO: Create alphabet model         X
    # TODO: Load katakana data            X
        # TODO: Commit to github          X
        # TODO: Remove comments           X
        # TODO: Recommit to github        X
        # TODO: Make call with preprocess X
        # TODO: Load 1C and 9B and add    X
        # TODO: Make postprocessing call  X
    # TODO: Train alphabet model          X
    # TODO: Train for hira, kata          X
    # TODO: Recognize points and commas   X
    # TODO: Clean files                   X
    # TODO: Add GUI
        # TODO: Add instructions          X
        # TODO: Add display page          X
        # TODO: Add translation control
        # TODO: Refresh using javascript
        # TODO: Add segmentation settings
        # TODO: Add words counter
        # TODO: Add anki exporter
    # TODO: Fix discriminator             X # Removed
    # TODO: Fix full model kata classes   X
    # TODO: Add handling for vert hyphens
    #       Currently recognized as RI
    # TODO: Remove trailing characters    X
    # TODO: Add translator                X
    # TODO: Improve kanji transcription   X
    # TODO: Add automatic juman server    X
    # TODO: Improve positionning
    # TODO: Add automated segmentation tuning
    # TODO: Add RNN
    # TODO: Prune model weights to improve memory footprint
    # TODO: Add element model
    # TODO: Integrate with makura japanese, save sentence samples
    # TODO: Makura japanese unlock skills, manually or through immersion
    # (golden petals)

    bbox = (212, 155, 655, 960)
    line_width = 45
    char_min_size = 26
    char_max_size = 32
    reader_helper = ReaderHelper(
        bbox, line_width, [char_min_size, char_max_size])
    image = reader_helper.draw()
    image.show()
