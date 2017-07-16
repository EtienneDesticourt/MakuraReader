from renderer import Renderer
from kindle_reader import KindleReader
from naive_segmenter import NaiveSegmenter
from collections import namedtuple
from recognizer import Recognizer
from tokenizer import Tokenizer, Token
import time
import threading
from ui.token_table_generator import TokenTableGenerator
import sys

FULL_MODEL    = "weights\\CNN_FULL_M7_2.09-0.979-0.069.h5"
FULL_LABELS   = "weights\\labels_full.npy"
OUTPUT_PATH = "ui\\images\\generated.png"


Character = namedtuple('Character', ['segment', 'text'])


class ReaderHelper(object):

    def __init__(self, kindle_bbox, line_width, char_size_range, output_path = OUTPUT_PATH):
        self.reader = KindleReader()
        self.segmenter = NaiveSegmenter()
        self.tokenizer = Tokenizer()
        self.renderer = Renderer()
        self.recognizer = Recognizer()
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
                # image.save(self.output_path,"PNG")
            time.sleep(1)

    def draw(self):
        image = self.reader.capture_kindle()
        characters = self.segmenter.get_characters(image)
        characters = [character for character in characters if not self.recognizer.is_blank(character.image)]        
        characters = self.recognizer.transcribe(characters)
        text = "".join([char.text for char in characters])
        tokens = self.tokenizer.tokenize(text)
        image = self.renderer.render(characters, tokens)
        tok_gen = TokenTableGenerator("data\\images")
        tok_gen.generate()
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
    # TODO: Add translator                
    # TODO: Improve kanji transcription   X
    # TODO: Add automatic juman server    X
    # TODO: Improve positionning          
    # TODO: Add automated segmentation tuning
    # TODO: Add RNN                       
    # TODO: Prune model weights to improve memory footprint
    # TODO: Add element model             
    # TODO: Integrate with makura japanese, save sentence samples
    # TODO: Makura japanese unlock skills, manually or through immersion (golden petals)


    bbox = (212, 155, 655, 960)
    line_width = 45
    char_min_size = 26
    char_max_size = 32
    reader_helper = ReaderHelper(bbox, line_width, [char_min_size, char_max_size])
    image = reader_helper.draw()
    image.show()