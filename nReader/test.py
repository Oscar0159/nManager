from requests_html import HTMLSession
from PyQt5 import QtWidgets, QtCore, QtGui

from ui.testUi import MainWindowUi

class UrlButton(QtWidgets.QPushButton):

    cked = QtCore.pyqtSignal(str)

    def __init__(self, name, text='', parent=None):
        super(UrlButton, self).__init__(text=text, parent=parent)
        self.url = 'https://nhentai.net/'
        self.setObjectName(name)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = MainWindowUi()
        self.ui.setup(self)

    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        self.addButton()

    def addButton(self):
        button = QtWidgets.QPushButton('test')
        self.ui.main_vlayout.addWidget(button)


if __name__ == '__main__':
    pass