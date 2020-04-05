from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
from ui.testUi import UiMainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)



if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication([])
    window = MainWindow()
    with open('./ui/test.qss', 'r') as file:
        app.setStyleSheet(file.read())
    window.show()
    sys.exit(app.exec_())