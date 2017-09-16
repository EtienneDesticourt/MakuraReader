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
import sys
import traceback

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
logger.info("Application started.")

def exception_handler(etype, value, tb):
    # TODO: Add pyqt warning dialog
    # "A critical error has occured. You may keep using the software
    # but utilization may be degraded. Restart of the Makura Reader is
    # recommended." or something to that effect
    logger.critical("Uncaught exception.\n --------------%s------------" % "".join(traceback.format_exception(etype,value,tb)))

sys.excepthook = exception_handler

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
