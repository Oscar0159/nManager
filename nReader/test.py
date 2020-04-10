from PyQt5 import QtCore, QtGui, QtWidgets

from ui.testUi import MainWindowUi
from ui.PageUi import PageWindow, NormalPage, GalleryPage, BookPage

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = MainWindowUi()
        self.ui.setupUi(self)

        self.my_page = {}

        self.ui.add_pagination_button.clicked.connect(self.addMainPage)
        self.ui.add_pagination_button.click()

    def addMainPage(self):
        self.register(BookPage(), 'main')
        self.goto('main')

    def addPage(self):
        pass

    def addPageButton(self):
        pass

    def register(self, widget, name):
        self.my_page[name] = widget
        self.ui.main_stack_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    def goto(self, name):
        if name in self.my_page:
            widget = self.my_page[name]
            self.ui.main_stack_widget.setCurrentWidget(widget)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    with open('./ui/test.qss', 'r') as file:
        app.setStyleSheet(file.read())

    w = Window()
    w.show()
    sys.exit(app.exec_())