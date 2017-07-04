from renderer import Renderer
from kindle_reader import KindleReader
from collections import namedtuple
from recognizer import Recognizer
from tokenizer import Tokenizer
import time
import threading

Character = namedtuple('Character', ['segment', 'text'])

DEFAULT_READER = KindleReader
DEFAULT_RENDERER = Renderer
DEFAULT_RECOGNIZER = Recognizer
DEFAULT_TOKENIZER = Tokenizer

DISCR_MODEL   = "weights\\CNN_K_M7_2_DISC.24-0.995-0.013.h5"
KAN_HI_MODEL  = "weights\\CNN_K_M7_2_KAN_HI.21-0.987-0.041.h5"
KATA_MODEL    = "weights\\CNN_K_M7_2_KATA.24-0.985-0.057.h5"
KAN_HI_LABELS = "weights\\kan_hi_labels.npy"
KATA_LABELS   = "weights\\kata_labels.npy"
FULL_MODEL    = "weights\\CNN_FULL_M7_2.09-0.979-0.069.h5"
FULL_LABELS   = "weights\\labels_full.npy"

OUTPUT_PATH = "ui\\images\\generated.png"

class ReaderHelper(object):

    def __init__(self, kindle_bbox, line_width, char_size_range, Reader=DEFAULT_READER,
        Renderer=DEFAULT_RENDERER,
        Recognizer=DEFAULT_RECOGNIZER,
        Tokenizer=DEFAULT_TOKENIZER,
        output_path = OUTPUT_PATH):
        self.reader = Reader(kindle_bbox, line_width, char_size_range)
        image_size = self.reader.get_size()
        if self.reader.background_is_white():
            background = (255, 255, 255)
            text_color = (0, 0, 0)
        else:
            background = (0, 0, 0)
            text_color = (255, 255, 255)
        self.tokenizer = Tokenizer()
        self.renderer = Renderer(image_size, line_width, background, text_color)
        self.recognizer = Recognizer(background_color=background)
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
                image.save(self.output_path,"PNG")
            time.sleep(1)

    def draw(self):
        characters = [Character(segment, text="ka") for segment in self.reader.get_characters()]
        text = self.recognizer.transcribe([character.segment.image for character in characters])
        with open("tempresult.txt", "w", encoding="utf8") as f:
            f.write(text)
        tokens = self.tokenizer.get_kana(text, characters)
        image = self.renderer.render(characters, tokens)
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