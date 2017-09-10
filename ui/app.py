from PyQt5.QtWidgets import QApplication
from ui.application import Application


def start_app(makura_reader):
    app = QApplication([])
    wrapper = Application(makura_reader)
    wrapper.start()
    app.exec_()