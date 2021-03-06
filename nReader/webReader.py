# -*- coding: utf-8 -*-
import os
import time
import sys
from queue import Queue
import requests
from threading import Thread

from PyQt5.QtWinExtras import QtWin
from requests_html import HTMLSession
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from ui.webReaderUi import UiMainWindow, ImageWidget


NHENTAI = 'https://nhentai.net/'
I_NHENTAI = 'https://i.nhentai.net/galleries/'  # 原始圖檔目錄
T_NHENTAI = 'https://t.nhentai.net/galleries/'   # 預覽圖檔目錄


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)


        self._thread_num = 5
        self.download_queue = Queue()
        self.http_url = ''
        self.label_list = []
        self.pixmap_list = []


        self.imageWidget = []

        self.scaleFactor = 1.0



        self.loadNhentai()
        self.addPreviewImage()
        self.loadPreviewImage()

        # signal connect
        self.ui.NumLineEdit.returnPressed.connect(self.startDisplay)
        self.ui.downloadButton.clicked.connect(self.zoomOut)
        self.ui.downloadButton_1.clicked.connect(self.zoomIn)
        self.ui.downloadButton_2.clicked.connect(self.open_dir)


    # def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
    #     # print(f'{a0.key()}')
    #     print('key')
    #
    # def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
    #     # print(f'{a0.type()}')
    #     print('mouse')
    #
    # def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
    #     # print(f'{a0.type()}')
    #     print('wheel')

    def zoomOut(self):
        self._scaleImage(-0.1)

    def zoomIn(self):
        self._scaleImage(0.1)

    def resetSize(self):
        self._scaleImage(1-self.scaleFactor)

    def _scaleImage(self, factor):
        self.scaleFactor += factor
        # print(f'factor:{self.scaleFactor}')
        for i in range(int(self.page_num)):
            # t = Thread(target=self.scale, args=(i,))
            # t.start()
            if not self.pixmap_list[i].isNull():    # 已載圖片的重新縮放
                w = self.pixmap_list[i].width() * self.scaleFactor
                h = self.pixmap_list[i].height() * self.scaleFactor
                self.label_list[i].setPixmap(self.pixmap_list[i].scaled(w, h, Qt.KeepAspectRatio))
        self.adjustScrollBar(self.ui.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.ui.scrollArea.verticalScrollBar(), factor)

    def scale(self, i):
        if not self.pixmap_list[i].isNull():  # 已載圖片的重新縮放
            self.label_list[i].resize(self.scaleFactor * self.label_list[i].pixmap().size())
            print(self.ui.formLayout.geometry())

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(scrollBar.value() + ((scrollBar.value() + (scrollBar.pageStep() / 2)) / ((self.scaleFactor -1) * 10 + (10 - 10 * factor)) * factor * 10)))

    def loadNhentai(self):
        self.http_url = NHENTAI
        session = HTMLSession()
        result = session.get(self.http_url)
        img_list = result.html.find('div.container div.gallery a img.lazyload', first=False)
        self.page_num = len(img_list)
        for element_img in img_list:
            image_url = element_img.attrs['data-src']
            self.download_queue.put(image_url, block=False)

    def addPreviewImage(self):
        for i in range(int(self.page_num)):
            self.imageWidget.append(ImageWidget())
            self.ui.formLayout.addWidget(self.imageWidget[i])

        # for i in range(int(self.page_num)):
        #     self.pixmap_list.append(QtGui.QPixmap())
        #     self.label_list.append(QtWidgets.QLabel())
        #     sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        #     self.label_list[i].setSizePolicy(sizePolicy)
        #     self.label_list[i].setAlignment(QtCore.Qt.AlignCenter)
        #     self.label_list[i].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        #     #self.ui.formLayout.addRow()
        #     self.ui.formLayout.addWidget(self.label_list[i])
        #     # self.ui.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_list[i])

    def loadPreviewImage(self):
        for i in range(int(self.page_num)):
            img_url = self.download_queue.get()
            self.imageWidget[i].setupImage(img_url)

        # for i in range(int(self.page_num)):
        #     img_url = self.download_queue.get()
        #     img_data = requests.get(img_url)
        #     self.pixmap_list[i].loadFromData(img_data.content)
        #     if not self.pixmap_list[i].isNull():
        #         w = 250
        #         self.label_list[i].setPixmap(self.pixmap_list[i].scaledToWidth(w))
        #         self.label_list[i].setStyleSheet('background-color: #1d1f21')


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
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.label_list[i].setSizePolicy(sizePolicy)
            self.label_list[i].setAlignment(QtCore.Qt.AlignCenter)
            # self.ui.formLayout.insertRow(i, self.label_list[i])
            self.ui.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_list[i])

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

    def clearWindow(self):
        self.label_list.clear()
        self.pixmap_list.clear()
        for i in range(self.ui.formLayout.count()):
            self.ui.formLayout.itemAt(i).widget().close()

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

    widget.grabKeyboard()
    sys.exit(app.exec_())
