from PyQt5.QtWidgets import QApplication

from reader_helper import ReaderHelper
from ui.application import Application

reader_helper = ReaderHelper()
reader_helper.start()

app = QApplication([])
wrapper = Application()
wrapper.start()
app.exec_()
reader_helper.stop()