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

from ui.mainUi import UiMainWindow

I_NHENTAI = 'https://i.nhentai.net/galleries/'  # 原始圖檔目錄


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)


        self._save_dir = os.getcwd() + os.sep + 'download'
        self._thread_num = 5
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

    def setAero(self, Qwin):
        if Qwin.isCompositionEnabled():
            Qwin.extendFrameIntoClientArea(-1, -1, -1, -1)
            Qwin.setAttribute(Qt.WA_TranslucentBackground, True)
            Qwin.setAttribute(Qt.WA_NoSystemBackground, False)
            Qwin.setStyleSheet("widget { background: transparent; }")
        else:
            QtWin.resetExtendedFrame(self)
            Qwin.setAttribute(Qt.WA_TranslucentBackground, False)
            #Qwin.setStyleSheet(QString("widget { background: %1; }").arg(QtWin::realColorizationColor().name()))

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
    #
    # def adjustScrollBar(self, scrollBar, factor):
    #     scrollBar.setValue(int(factor * scrollBar.value()
    #                            + ((factor - 1) * scrollBar.pageStep() / 2)))

    def scale(self, i):
        if not self.pixmap_list[i].isNull():  # 已載圖片的重新縮放
            self.label_list[i].resize(self.scaleFactor * self.label_list[i].pixmap().size())
            print(self.ui.formLayout.geometry())

    def adjustScrollBar(self, scrollBar, factor):
        # print(f'滾輪位置:{scrollBar.value()}')
        # print(f'滾窗大小: {scrollBar.pageStep()}')
        scrollBar.setValue(int(scrollBar.value() + ((scrollBar.value() + (scrollBar.pageStep() / 2)) / ((self.scaleFactor -1) * 10 + (10 - 10 * factor)) * factor * 10)))
        # print(f'after滾輪位置: {scrollBar.value()}')

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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    with open('./ui/style.qss', 'r') as file:
        app.setStyleSheet(file.read())

    widget.show()
    sys.exit(app.exec_())
