from PyQt5 import QtCore, QtGui, QtWidgets

from ui.nManagerUi import MainWindowUi
from pageManager import NormalPage, GalleryPage, BookPage


class PageButton(QtWidgets.QPushButton):
    gotoSignal = QtCore.pyqtSignal(str)
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.clicked.connect(self.goto)

    def goto(self):
        self.gotoSignal.emit(self.name)


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = MainWindowUi()
        self.ui.setupUi(self)
        self.my_page = {}
        self.addMainPage()
        self.ui.add_pagination_button.clicked.connect(self.addPage)

    def addMainPage(self):
        name = 'nhentai'
        url = 'https://nhentai.net/'
        self.register(name, NormalPage)
        self.goto(name)
        self.my_page[name].setUrl(url)
        self.my_page[name].setup()

    def addPage(self):
        name = 'test'
        url = 'https://nhentai.net/?page=11'
        self.register(name, NormalPage)
        self.goto(name)
        self.my_page[name].setUrl(url)
        self.my_page[name].setup()

    def addPageButton(self, name):
        Button = PageButton(name)
        Button.gotoSignal.connect(self.goto)
        Button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.ui.pagination_hlayout.insertWidget(len(self.my_page)-1, Button)

    def register(self, name, page):
        # if name is exist in my_page
        self.my_page[name] = page()
        self.ui.main_stack_widget.addWidget(self.my_page[name])
        self.addPageButton(name)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.my_page:
            widget = self.my_page[name]
            self.ui.main_stack_widget.setCurrentWidget(widget)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    with open('ui/nManager.qss', 'r') as file:
        app.setStyleSheet(file.read())

    w = Window()
    w.show()
    sys.exit(app.exec_())