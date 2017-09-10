

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
        self.recognizer = recognizer
        self.tokenizer = tokenizer
        self.recorder = recorder
        self.history = history

    def save_page_to_history(self, tokens):
        for token in tokens:
            if token.is_punctuation() or token.is_single_letter():
                continue
            self.history.add_word(token)

    def capture_page(self):
        return self.recorder.capture()

    @property
    def new_page_callback(self):
        return self.recorder.new_page_callback

    @new_page_callback.setter
    def new_page_callback(self, callback):
        self.recorder.new_page_callback = callback

    def read_page(self):
        """Reads the page currently displayed on screen.

        # Returns
            A list of tokens.
        """
        page_image = self.capture_page()
        texts = self.recognizer.transcribe(page_image)
        tokens = [tk for text in texts for tk in self.tokenizer.split(text)]
        return tokens
