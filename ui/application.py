from PyQt5.QtCore import QUrl, QObject, pyqtSlot
# from PySide.QtCore import Slot as pyqtSlot
import os

from ui.widgets.skinned_title_bar import SkinnedTitleBar
from ui.main_dialog import MainDialog
import ui.utils
import threading

import time


class Application(QObject):
    INDEX_URL = "ui\\html\\index.html"
    INTRODUCTION_URL = "ui\\html\\introduction.html"

    def __init__(self, reader_helper):
        QObject.__init__(self)
        self.dialog = MainDialog()
        self.bridge = Bridge(self.dialog.view,
                             self.generate_page,
                             utils.ui.generate_token_definition_html)
        # self.dialog.add_js_object(self, "wrapper")
        self.reader_helper = reader_helper
        self.running = False
        self.tokens = None

    def generate_page(self, furigana=False, translation=False):
        tokens = self.reader_helper.get_tokens()
        html = ui.utils.generate_page_html(tokens, furigana, translation)
        return html

    def check_for_new_page(self):
        while self.running:
            if self.reader_helper.page_has_changed():
                #TODO: Set loading screen
                html = self.generate_page()
                self.bridge.set_book_page(html)

            time.sleep(1)

    def stop(self):
        self.running = False

    def start(self):
        self.running = True
        t = threading.Thread(target=self.check_for_new_page)
        t.start()
        self.load_url(self.INTRODUCTION_URL)
        self.dialog.show()

    def load_url(self, url):
        path = self.build_qurl(url)
        self.dialog.load_page(path)

    def build_qurl(self, local_file):
        path = os.path.join(os.getcwd(), local_file)
        path = QUrl.fromLocalFile(path)
        return path
