from PyQt5.QtWidgets import QApplication
from ui.application import Application
import tests.ocr.mock_recognizer
import tests.text.mock_tokenizer
import makura_reader
import history
import recorder
import config
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
logger.info("Application started.")

tokenizer = tests.text.mock_tokenizer.MockTokenizer()
recognizer = tests.ocr.mock_recognizer.MockRecognizer()

history = history.History(**config.history_config)
recorder = recorder.Recorder(**config.recorder_config)
reader = makura_reader.MakuraReader(recognizer, tokenizer, recorder, history)

app = QApplication([])
wrapper = Application(reader)
wrapper.start()
app.exec_()

logger.info("Application stopped.")
logger.info("--------------------")
