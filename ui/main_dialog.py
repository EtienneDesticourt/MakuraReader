from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtWebChannel import QWebChannel

from ui.widgets.skinned_title_bar import SkinnedTitleBar


class MainDialog(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.title_bar = SkinnedTitleBar(
            parent=self, height=20, color_hex="#1E262B")
        self.view = QWebView()
        layout = QVBoxLayout()
        layout.addWidget(self.title_bar)
        layout.addWidget(self.view)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def load_page(self, url):
        self.view.load(url)
