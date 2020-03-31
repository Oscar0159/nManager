# -*- coding: utf-8 -*-
import time
from threading import Thread
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from queue import Queue

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from requests_html import HTMLSession
from ui.mainUi import Ui_MainWindow

iNhentai = 'https://i.nhentai.net/galleries/'  # 原始圖檔目錄

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._thread_num = 10
        self.num = ''
        self.gallery_id = ''
        self.page_num = ''
        self.download_queue = Queue()
        self.http_url = ''
        self.labelList = []
        self.piximap = []

        self.scaleFactor = 1.0

        # signal connect
        self.ui.NumLineEdit.returnPressed.connect(self.startDisplay)
        self.ui.downloadButton.clicked.connect(self.zoomOut)

    # def paintEvent(self, QPaintEvent):
    #     #print('paintEvent')
    #     pass
    #
    # def resizeEvent(self, QResizeEvent):
    #     print(self.ui.groupBox.size())
    #     self.resizeImage()
    #
    # def resizeImage(self):
    #     for i in self.labelList:
    #         print(self.ui.scrollArea.size())
    #         #QtWidgets.QLabel.resize(self.scrollArea.size())
    #         i.resize(self.ui.scrollArea.size())

    def zoomOut(self):
        self.scaleImage(0.8)


    def scaleImage(self, factor):
        self.scaleFactor *= factor
        for i in range(int(self.page_num)):
            # print(type(i.size()))
            print(self.piximap[i].size())
            self.labelList[i].setPixmap(self.piximap[i].scaled(200, 600, Qt.KeepAspectRatio))
            # i.resize(self.scaleFactor * i.pixmap().size())
            # i.setAlignment(QtCore.Qt.AlignCenter)

        #self.ui.groupBox.setGeometry(0, 0, self.ui.groupBox.geometry().width(), self.ui.groupBox.geometry().height() * self.scaleFactor)


        self.adjustScrollBar(self.ui.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.ui.scrollArea.verticalScrollBar(), factor)


        self.ui.groupBox.updateGeometry()
        #print(1 * 0.8)
        #print(self.ui.groupBox.geometry())
        # print(self.ui.groupBox.geometry().width())
        # print(self.ui.groupBox.geometry().height())



    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def startDisplay(self):
        self.num = self.ui.NumLineEdit.text()  # 取得編號
        self.ui.NumLineEdit.clear()    # 清除輸入區
        self.http_url = 'https://nhentai.net/g/' + self.num + '/'
        self._getData()    # 取得畫廊編號, 頁數, 所有圖片下載位置
        self.putImgInLayout()

    def _getData(self):
        try:
            session = HTMLSession()
            result = session.get(self.http_url)  # 使用GET取得網頁資料
            self.gallery_id = result.html.search('"media_id":"{}"')[0]  # 取得畫廊編號
            self.page_num = result.html.search('<div>{} pages</div>')[0]  # 取得頁數
            img_list = result.html.find('div.container#thumbnail-container div a img.lazyload', first=False)
            for element_img in img_list:  # 儲存圖片下載位置
                substr = element_img.attrs['data-src'].split('/')[-1].split('.')
                img_index = substr[0][:-1]  # 頁數
                img_format = substr[1]  # 檔案類型
                image_url = iNhentai + self.gallery_id + '/' + img_index + '.' + img_format
                self.download_queue.put(image_url, block=False)
        except Exception as e:
            print(f'取得資料錯誤 ： {e}')
            time.sleep(0.5)

    def putImgInLayout(self):
        for i in range(int(self.page_num)):
            self.piximap.append(QtGui.QPixmap())
            self.labelList.append(QtWidgets.QLabel())
            self.labelList[i].setScaledContents(True)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.labelList[i].sizePolicy().hasHeightForWidth())
            self.labelList[i].setSizePolicy(sizePolicy)
            self.labelList[i].setAlignment(QtCore.Qt.AlignCenter)
            self.ui.formLayout.insertRow(i, self.labelList[i])

        for i in range(self._thread_num):
            t = Thread(target=self.loadImg)
            t.setDaemon(True)
            t.start()

    def loadImg(self):
        while not self.download_queue.empty():
            img_url = self.download_queue.get()
            substr = img_url.split('/')[-1].split('.')
            img_index = int(substr[0])
            img_data = requests.get(img_url)
            self.piximap[img_index - 1].loadFromData(img_data.content)
            self.labelList[img_index - 1].setPixmap(self.piximap[img_index - 1])
        # while not self.download_queue.empty():
        #     img_url = self.download_queue.get()
        #     substr = img_url.split('/')[-1].split('.')
        #     img_index = int(substr[0])
        #     img_data = requests.get(img_url)
        #     piximap = QtGui.QPixmap()
        #     piximap.loadFromData(img_data.content)
        #     self.labelList[img_index - 1].setPixmap(piximap)

    def msg(self):
        QtWidgets.QMessageBox.information(self, 'title', 'msg', QtWidgets.QMessageBox.Yes)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()

    with open('./ui/style.qss', 'r') as file:
        app.setStyleSheet(file.read())

    widget.show()
    sys.exit(app.exec_())