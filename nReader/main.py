# -*- coding: utf-8 -*-
import os
import time
import sys
from queue import Queue
import requests
from threading import Thread

from requests_html import HTMLSession
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from ui.mainUi import UiMainWindow

I_NHENTAI = 'https://i.nhentai.net/galleries/'  # 原始圖檔目錄


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.createActions()

        self._save_dir = os.getcwd() + os.sep + 'download'
        self._thread_num = 10
        self._serial_num = ''
        self.gallery_id = ''
        self.page_num = '0'
        self.download_queue = Queue()
        self.http_url = ''
        self.label_list = []
        self.pixmap_list = []

        self.scaleFactor = 1.0

        # signal connect
        self.ui.NumLineEdit.returnPressed.connect(self.startDisplay)
        self.ui.downloadButton.clicked.connect(self.zoomOut)
        self.ui.downloadButton_1.clicked.connect(self.zoomIn)
        self.ui.downloadButton_2.clicked.connect(self.open_dir)

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
        self._scaleImage(-0.1)

    def zoomIn(self):
        self._scaleImage(0.1)

    def resetSize(self):
        self._scaleImage(1-self.scaleFactor)

    def _scaleImage(self, factor):
        self.scaleFactor += factor
        print(self.scaleFactor)
        for i in range(int(self.page_num)):
            # t = Thread(target=self.scale, args=(i,))
            # t.start()
            if not self.pixmap_list[i].isNull():    # 已載圖片的重新縮放
                w = self.pixmap_list[i].width() * self.scaleFactor
                h = self.pixmap_list[i].height() * self.scaleFactor
                self.label_list[i].setPixmap(self.pixmap_list[i].scaled(w, h, Qt.KeepAspectRatio))
        self.adjustScrollBar(self.ui.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.ui.scrollArea.verticalScrollBar(), factor)
    #
    # def adjustScrollBar(self, scrollBar, factor):
    #     scrollBar.setValue(int(factor * scrollBar.value()
    #                            + ((factor - 1) * scrollBar.pageStep() / 2)))

    def scale(self, i):
        if not self.pixmap_list[i].isNull():  # 已載圖片的重新縮放
            self.label_list[i].resize(self.scaleFactor * self.label_list[i].pixmap().size())
            print(self.ui.formLayout.geometry())

    def adjustScrollBar(self, scrollBar, factor):
        print(scrollBar.value())
        print(f'pageStep: {scrollBar.pageStep()}')
        scrollBar.setValue(int(scrollBar.value() + (self.scaleFactor - 1) * scrollBar.pageStep() / 2))
        print(f'after: {scrollBar.value()}')

    def startDisplay(self):
        self._serial_num = self.ui.NumLineEdit.text()
        self.ui.NumLineEdit.clear()
        self.http_url = 'https://nhentai.net/g/' + self._serial_num + '/'
        self._getData()
        self._addImgLabel()

        for i in range(self._thread_num):
            t = Thread(target=self._loadImg)
            t.setDaemon(True)
            t.start()

    def _getData(self):
        try:
            session = HTMLSession()
            result = session.get(self.http_url)
            self.gallery_id = result.html.search('"media_id":"{}"')[0]
            self.page_num = result.html.search('<div>{} pages</div>')[0]
            img_list = result.html.find('div.container#thumbnail-container div a img.lazyload', first=False)
            for element_img in img_list:
                substr = element_img.attrs['data-src'].split('/')[-1].split('.')
                img_index = substr[0][:-1]
                img_format = substr[1]
                image_url = I_NHENTAI + self.gallery_id + '/' + img_index + '.' + img_format
                self.download_queue.put(image_url, block=False)
        except Exception as e:
            print(f'取得資料錯誤： {e}')
            time.sleep(0.5)

    def _addImgLabel(self):
        for i in range(int(self.page_num)):
            self.pixmap_list.append(QtGui.QPixmap())
            self.label_list.append(QtWidgets.QLabel())
            # self.label_list[i].setScaledContents(True)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            self.label_list[i].setSizePolicy(sizePolicy)
            self.label_list[i].setAlignment(QtCore.Qt.AlignCenter)
            # self.ui.formLayout.insertRow(i, self.label_list[i])
            self.ui.formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, self.label_list[i])

    def _loadImg(self):
        while not self.download_queue.empty():
            img_url = self.download_queue.get()
            img_index = int(img_url.split('/')[-1].split('.')[0])
            img_data = requests.get(img_url)
            self.pixmap_list[img_index-1].loadFromData(img_data.content)
            if not self.pixmap_list[img_index-1].isNull():
                w = self.pixmap_list[img_index-1].width() * self.scaleFactor
                h = self.pixmap_list[img_index-1].height() * self.scaleFactor
                self.label_list[img_index-1].setPixmap(self.pixmap_list[img_index-1].scaled(w, h, Qt.KeepAspectRatio))

    def createActions(self):
        self.zoomInAct = QtWidgets.QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=True, triggered=self.zoomIn)
        self.zoomOutAct = QtWidgets.QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=True, triggered=self.zoomOut)
        self.resetSizeAct = QtWidgets.QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=True, triggered=self.resetSize)
        #self.fitToWindowAct = QtWidgets.QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

    def msg(self):
        QtWidgets.QMessageBox.information(self, 'title', 'msg', QtWidgets.QMessageBox.Yes)

    def open_dir(self):
        path = os.getcwd()
        os.system(f'explorer.exe {path}')

    def _createFolder(self):
        try:
            if (not os.path.exists(self._save_dir)):  # 建立下載目錄
                os.mkdir(self._save_dir)

            if (os.path.exists(self._save_dir)):  # 下載目錄存在
                self._save_path = self._save_dir + os.sep + str(self._serial_num)
                if (not os.path.exists(self._save_path)):  # 建立下載目標資料夾
                    os.mkdir(self._save_path)
                else:  # 下載目標資料夾存在 -> 下載缺少的圖片
                    pass
        except Exception as e:
            print(f'創建資料夾錯誤 : {e}')
        else:
            print(f'創建資料夾 : {self._serial_num}  位置:{self._save_path}')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    with open('./ui/style.qss', 'r') as file:
        app.setStyleSheet(file.read())

    widget.show()
    sys.exit(app.exec_())