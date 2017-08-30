

class Bridge(object):
    """Wrapper for the Javascript functions and bridge to be called by them.

    # Arguments
        name: The name to be given to the bridge.
    """

    def __init__(self, view,
                 load_page_callback,
                 load_definition_callback,
                 name="wrapper"):
        self.channel = QWebChannel()
        self.channel.registerObject(name, self)
        self.page = view.page()
        self.page.setWebChannel(self.channel)
        self.get_book_page = load_page_callback
        self.get_token_definition = load_definition_callback
        self.translation_toggled = False

    def run_js(self, code):
        self.page.runJavaScript(code)

    @pyqtSlot()
    def load_book_page(self, furigana=False, translation=False):
        def async_load():
            html = self.get_book_page(furigana, translation)
            self.set_book_page(html)
        threading.Thread(target=async_load).start()

    @pyqtSlot(str)
    def load_token_definition(self, token):
        html = self.get_token_definition(token)
        self.set_token_definition(html)

    @pyqtSlot()
    def show_furigana(self):
        self.load_book_page(furigana=True)

    @pyqtSlot()
    def toggle_translation(self):
        if self.translation_toggled:
            self.load_book_page()
        else:
            self.load_book_page(translation=True)
        translation_toggled = not translation_toggled

    def set_book_page(self, html):
        self.run_js("set_book_page(\"%s\");" % html)

    def set_token_definition(self, html):
        self.run_js("set_token_definition(\"%s\");" % html)
