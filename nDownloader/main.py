from PyQt5.QtGui import QIntValidator, QValidator

from httpHandaler import DownloadHttpList
from threading import Thread
import sys
import os
from ui.mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
import time


def pt(var):
    print(type(var))
    print(var)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.http_list = DownloadHttpList()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    #   setupFunction
        self.ui.NumLineEdit.setValidator(QIntValidator(1, 999999))

        self.ui.pushButton.clicked.connect(self.openMenu)
        self.ui.pushButton_2.clicked.connect(self.exit)
        self.ui.NumLineEdit.returnPressed.connect(self.send)

        self.http_list.push_data.connect(self.pushTextBrowser)

    def closeEvent(self):
        self.timer.cancel()

    def send(self):
        number = self.ui.NumLineEdit.text()
        self.ui.NumLineEdit.clear()
        if number != '':
            self.http_list.num = number
            # t = Thread(target=self.http_list.pushHttp, args=(number,))
            # t.start()
            self.http_list.start()

    def openMenu(self):
        path = os.getcwd()
        os.system("explorer.exe %s" % path)

    def exit(self):
        #qApp = QtWidgets.QApplication.instance(self)
        #qApp.quit()
        pass

    def numLineInput(self):
        # pt(self.ui.NumLineEdit.text())
        # self.ui.NumLineEdit.clear()
        self.send()

    def pushTextBrowser(self, text):
        self.ui.textBrowser.append(text)
        QtWidgets.QApplication.processEvents()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())







    # http_list = DownloadHttpList()
    # #http_list.setDownloadMaxNum(2)   # 最多幾本同時下載
    #
    # while True:
    #     number = input('輸入神秘六位數:')
    #     t = Thread(target=http_list.pushHttp, args=(number,))   # 接受持續輸入
    #     t.start()