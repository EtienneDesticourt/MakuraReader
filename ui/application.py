from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
import threading
import logging
import time
import os
import ui.utils


class Application(QWidget):
    """A bridge object between the HTML/CSS/JS frontend and the python backend
    using the pyqt library.

    # Arguments
        makura_reader: The backend reader.
    """
    INDEX_URL = "ui\\html\\index.html"
    INTRODUCTION_URL = "ui\\html\\introduction.html"

    def __init__(self, makura_reader):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Creating application instance.")

        # Setup layout
        self.view = QWebView()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Setup bridge to JS
        self.channel = QWebChannel()
        self.channel.registerObject("wrapper", self)
        self.page = self.view.page()
        self.page.setWebChannel(self.channel)

        self.makura_reader = makura_reader
        self.makura_reader.new_page_callback = self.reload_book_page
        self.tokens = None
        self.page_vocabulary = []
        self.translation_toggled = False

    def start(self):
        self.load_url(self.INTRODUCTION_URL)
        self.show()

    def load_url(self, url):
        self.logger.info("Loading page %s." % url)
        path = self.build_qurl(url)
        self.view.load(path)

    def build_qurl(self, local_file):
        path = os.path.join(os.getcwd(), local_file)
        path = QUrl.fromLocalFile(path)
        return path

    def run_js(self, code):
        self.page.runJavaScript(code)

    def gen_book_page(self, reload_page=False, furigana=False, translation=False):
        self.logger.info("User asked for page modification: %s." % {"reload_page": reload_page, "furigana":furigana, "translation":translation})
        if reload_page or not self.tokens:
            self.tokens = self.makura_reader.read_page()
            self.page_vocabulary = self.makura_reader.save_page(self.tokens)
            self.set_num_new_words(len(self.page_vocabulary))
            self.set_num_words_total(self.makura_reader.vocabulary_size)
        html = ui.utils.generate_page_html(self.tokens, furigana, translation)
        return html

    @pyqtSlot()
    def reload_book_page(self):
        self.show_book_page(reload=True)

    @pyqtSlot()
    def show_book_page(self, reload=False, furigana=False, translation=False):
        def async_load():
            html = self.gen_book_page(reload, furigana, translation)
            self.set_book_page(html)
        threading.Thread(target=async_load).start()

    @pyqtSlot(int)
    def load_token_definition(self, token_index):
        self.logger.info("User asked for token definition: %s." % self.tokens[token_index].base)
        html = ui.utils.generate_token_definition_html(self.tokens[token_index])
        self.set_token_definition(html)

    @pyqtSlot()
    def show_furigana(self):
        self.show_book_page(reload=False, furigana=True)

    @pyqtSlot()
    def toggle_translation(self):
        if self.translation_toggled:
            self.show_book_page(reload=False)
        else:
            self.show_book_page(reload=False, translation=True)
        self.translation_toggled = not self.translation_toggled

    @pyqtSlot()
    def export_csv(self):
        # log call from js
        # self.history.to_csv()
        pass

    def set_book_page(self, html):
        self.logger.info("Updating book page in JS.")
        self.run_js("set_book_page(\"%s\");" % html)

    def set_token_definition(self, html):
        self.logger.info("Updating token definition in JS.")
        self.run_js("set_token_definition(\"%s\");" % html)

    def set_num_words_total(self, html):
        self.logger.info("Updating number of words in JS.")
        self.run_js("set_num_words_total(\"%s\");" % html)

    def set_num_new_words(self, html):
        self.logger.info("Updating number of new words in JS.")
        self.run_js("set_num_new_words(\"%s\");" % html)
