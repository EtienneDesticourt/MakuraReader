from PyQt5.QtWidgets import QApplication

from reader_helper import ReaderHelper
from ui.application import Application

bbox = (212, 155, 655, 960)
line_width = 45
char_min_size = 26
char_max_size = 32
reader_helper = ReaderHelper(bbox, line_width, [char_min_size, char_max_size])
reader_helper.start()

app = QApplication([])
wrapper = Application()
wrapper.start()
app.exec_()
reader_helper.stop()