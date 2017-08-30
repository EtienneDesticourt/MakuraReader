from PyQt5.QtWidgets import QApplication

from reader_helper import ReaderHelper
from ui.application import Application

reader_helper = ReaderHelper()

app = QApplication([])
wrapper = Application(reader_helper)
wrapper.start()
app.exec_()
wrapper.stop()