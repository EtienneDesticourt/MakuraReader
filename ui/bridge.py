from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
import threading


class Bridge(QObject):
    """Wrapper for the Javascript functions and bridge to be called by them.

    # Arguments
        name: The name to be given to the bridge.
    """

    def __init__(self, view,
                 load_page_callback,
                 load_definition_callback,
                 history=None,
                 name="wrapper"):
        super().__init__()
        self.channel = QWebChannel()
        self.channel.registerObject(name, self)
        self.page = view.page()
        self.page.setWebChannel(self.channel)
        self.get_book_page = load_page_callback
        self.get_token_definition = load_definition_callback
        self.history = history
        self.translation_toggled = False

    def run_js(self, code):
        self.page.runJavaScript(code)

    @pyqtSlot()
    def update_tokens(self):
        print("fuck")
        self.load_book_page(reload=True)

    @pyqtSlot()
    def load_book_page(self, reload=False, furigana=False, translation=False):
        def async_load():
            html = self.get_book_page(reload, furigana, translation)
            self.set_book_page(html)
        threading.Thread(target=async_load).start()

    @pyqtSlot(int)
    def load_token_definition(self, token):
        print("fook")
        html = self.get_token_definition(token)
        self.set_token_definition(html)

    @pyqtSlot()
    def show_furigana(self):
        print("showing furigana.")
        self.load_book_page(reload=False, furigana=True)

    @pyqtSlot()
    def toggle_translation(self):
        print("showing translation.")
        if self.translation_toggled:
            self.load_book_page(reload=False)
        else:
            self.load_book_page(reload=False, translation=True)
        self.translation_toggled = not self.translation_toggled

    @pyqtSlot()
    def export_csv(self):
        # self.history.to_csv()
        pass

    def set_book_page(self, html):
        self.run_js("set_book_page(\"%s\");" % html)

    def set_token_definition(self, html):
        self.run_js("set_token_definition(\"%s\");" % html)

    def set_num_words_total(self, html):
        self.run_js("set_num_words_total(\"%s\");" % html)

    def set_num_new_words(self, html):
        self.run_js("set_num_new_words(\"%s\");" % html)
