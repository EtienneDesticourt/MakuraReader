import logging


class MakuraReader(object):
    """The Makura Reader can read and interpret any media
    written in japanese provided it's currently being displayed
    on screen.

    # Arguments
        recognizer: An instance that can transcribe an image into text.
        tokenizer: An instance that can split text into tokens.
        recorder: An instance that can capture an image of the media to be read.
        history: An instance that can save tokens to disk.
    """

    def __init__(self, recognizer, tokenizer, recorder, history):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Creating reader instance.")
        self.recognizer = recognizer
        self.tokenizer = tokenizer
        self.recorder = recorder
        self.history = history

    def load_history(self):
        self.history.load()

    def save_page(self, tokens):
        new_tokens = self.history.add_page(tokens)
        self.history.save()
        return new_tokens

    def capture_page(self):
        return self.recorder.capture()

    @property
    def new_page_callback(self):
        return self.recorder.new_page_callback

    @new_page_callback.setter
    def new_page_callback(self, callback):
        self.recorder.new_page_callback = callback

    @property
    def vocabulary_size(self):
        return len(self.history.words)

    def read_page(self):
        """Reads the page currently displayed on screen.

        # Returns
            A list of tokens.
        """
        self.logger.info("Reading page.")
        page_image = self.capture_page()
        texts = self.recognizer.transcribe(page_image)
        tokens = [tk for text in texts for tk in self.tokenizer.split(text)]
        return tokens


class MakuraReaderException(Exception):
    pass
