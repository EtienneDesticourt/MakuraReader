from PyQt5.QtCore import QUrl, QObject, pyqtSlot

import os

from ui.widgets.skinned_title_bar import SkinnedTitleBar
from ui.main_dialog import MainDialog

class Application(QObject):
    INDEX_URL = "ui\\html\\index.html"
    INTRODUCTION_URL = "ui\\html\\introduction.html"

    def __init__(self):
        QObject.__init__(self)
        self.dialog = MainDialog()

    def start(self):
        self.load_url(self.INTRODUCTION_URL)
        self.dialog.show()

    def load_url(self, url):
        path = self.build_qurl(url)
        self.dialog.load_page(path)

    def build_qurl(self, local_file):
        path = os.path.join(os.getcwd(), local_file)
        path = QUrl.fromLocalFile(path)
        return path
