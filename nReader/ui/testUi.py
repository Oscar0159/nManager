# -*- coding: utf-8 -*-
import requests

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (QApplication, QLayout, QPushButton, QSizePolicy,
        QWidget)
from PyQt5.QtWinExtras import QtWin


class UiMainWindow(object):
    def setupUi(self, MainWindow):

        # main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle('nReader')
        MainWindow.setMinimumWidth(400)
        MainWindow.setMinimumHeight(600)
        MainWindow.resize(600, 900)

        MainWindow.setWindowOpacity(0.95)

        # flow layout
        self.flowLayout = FlowLayout()

        # image widget
        self.imageWidget = []
        for i in range(1):
            self.imageWidget.append(ImageWidget())
            self.imageWidget[i].setupImage()
            self.flowLayout.addWidget(self.imageWidget[i])

        # QVBoxLayout
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.addLayout(self.flowLayout)

        # central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setLayout(self.vLayout)
        MainWindow.setCentralWidget(self.centralwidget)


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


class ImageWidget(QWidget):
    def __init__(self):
        super(ImageWidget, self).__init__()

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setText('ttestt')
        self.imageLabel.setStyleSheet('background-color: #563251;')
        self.verticalLayout.addWidget(self.imageLabel)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        # 語言圖示
        self.languageLabel = QtWidgets.QLabel()
        self.languageLabel.setStyleSheet('padding: 0px;')
        pixmap = QtGui.QPixmap('./icon/Japan.png')
        self.languageLabel.setPixmap(pixmap.scaledToHeight(20))
        #print(self.languageLabel.size())
        self.horizontalLayout.addWidget(self.languageLabel)

        # 標題
        self.captionLabel = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        #sizePolicy.setHeightForWidth(self.captionLabel.sizePolicy().hasHeightForWidth())
        self.captionLabel.setSizePolicy(sizePolicy)
        self.captionLabel.setScaledContents(True)
        self.captionLabel.setText('[Jajujo (Jovejun.)] Kiritan no Tadashii Shitsuke-kata. (VOICEROID) [Chinese] [moye个人汉化] [Digital]')
        self.captionLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.captionLabel.setWordWrap(True)
        self.horizontalLayout.addWidget(self.captionLabel)

        # 下載按鈕
        self.downloadButton = QtWidgets.QPushButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./icon/download_light.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton.setIcon(icon)

        #print(self.downloadButton.size())
        self.horizontalLayout.addWidget(self.downloadButton)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 20)
        self.horizontalLayout.setStretch(2, 1)


        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)

    def setupImage(self):
        img_url = 'https://t.nhentai.net/galleries/1594289/thumb.jpg'
        img_data = requests.get(img_url)
        pix = QtGui.QPixmap()
        pix.loadFromData(img_data.content)
        w = 250
        self.imageLabel.setPixmap(pix.scaledToWidth(w))