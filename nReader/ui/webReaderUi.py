# -*- coding: utf-8 -*-
import requests

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (QApplication, QLayout, QPushButton, QSizePolicy,
        QWidget)
from PyQt5.QtWinExtras import QtWin


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        # style
        with open('./ui/style.qss') as file:
            s = file.readline()
            #s = ''.join(s).strip('\n')
        MainWindow.setStyleSheet(s)

        # main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle('nReader')
        MainWindow.setMinimumWidth(400)
        MainWindow.setMinimumHeight(600)
        MainWindow.resize(600, 900)


        MainWindow.setWindowOpacity(0.95)
        #MainWindow.setWindowFlags(Qt.FramelessWindowHint)

        # QLineEdit
        self.NumLineEdit = QtWidgets.QLineEdit()
        self.NumLineEdit.setObjectName('NumLineEdit')
        self.NumLineEdit.setValidator(QtGui.QIntValidator(1, 999999))
        self.NumLineEdit.setPlaceholderText('xxxxxx')
        self.NumLineEdit.setGeometry(0, 0, 151, 28)
        self.NumLineEdit.setAlignment(QtCore.Qt.AlignCenter)

        # QFormLayout
        self.formLayout = FlowLayout()
        # self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        # self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)

        # self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        # self.formLayout.setLabelAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        # self.formLayout.setContentsMargins(0, 0, 0, 0)
        # pushSpacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.formLayout.setItem(0, QtWidgets.QFormLayout.FieldRole, pushSpacerItem)

        # QGroupBox
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.setStyleSheet('background-color: #263e52')
        self.groupBox.setLayout(self.formLayout)
        self.groupBox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # QScrollArea
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.groupBox)
        self.scrollArea.setWidgetResizable(True)

        # QCheckBox
        self.checkButton = QtWidgets.QCheckBox('自動下載')


        # QPushButton
        self.downloadButton = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy)
        self.downloadButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./icon/zoom_out.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton.setIcon(icon)

        self.downloadButton_1 = QtWidgets.QPushButton()
        self.downloadButton_1.setSizePolicy(sizePolicy)
        self.downloadButton_1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./icon/zoom_in.ico'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton_1.setIcon(icon)

        self.downloadButton_2 = QtWidgets.QPushButton()
        self.downloadButton_2.setSizePolicy(sizePolicy)
        self.downloadButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./icon/folder_light.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadButton_2.setIcon(icon)

        # QHBoxLayout
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.addWidget(self.downloadButton)
        self.hLayout.addWidget(self.downloadButton_1)
        self.hLayout.addWidget(self.downloadButton_2)
        spaceItem_L = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        #self.hLayout.addItem(spaceItem_L)
        self.hLayout.addWidget(self.NumLineEdit)
        spaceItem_R = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        #self.hLayout.addItem(spaceItem_R)
        self.hLayout.addWidget(self.checkButton)
        #self.hLayout.setStretch(3, 1)
        #self.hLayout.setStretch(4, )
        #self.hLayout.setStretch(5, 1)

        # page index in QHBoxLayout
        self.pageIndexLayout = QtWidgets.QHBoxLayout()
        self.indexButton = []
        for i in range(7):
            self.indexButton.append(QtWidgets.QPushButton(f'{i+1}'))
            self.pageIndexLayout.addWidget(self.indexButton[i])

        # page button in QHBoxLayout
        self.pageButtonLayout = QtWidgets.QHBoxLayout()
        self.firstButton = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/doubleLeft_light.png')))
        self.previousButton = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/left_light.png')))
        self.nextButton = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/right_light.png')))
        self.lastButton = QtWidgets.QPushButton(icon=QtGui.QIcon(QtGui.QPixmap('./icon/doubleRight_light.png')))
        self.pageButtonLayout.addWidget(self.firstButton)
        self.pageButtonLayout.addWidget(self.previousButton)
        self.pageButtonLayout.addLayout(self.pageIndexLayout)
        self.pageButtonLayout.addWidget(self.nextButton)
        self.pageButtonLayout.addWidget(self.lastButton)
        self.pageButtonLayout.setStretch(0, 1)
        self.pageButtonLayout.setStretch(1, 2)
        self.pageButtonLayout.setStretch(2, 10)
        self.pageButtonLayout.setStretch(3, 2)
        self.pageButtonLayout.setStretch(4, 1)

        # QVBoxLayout
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addWidget(self.scrollArea)
        self.vLayout.addLayout(self.pageButtonLayout)

        # central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setLayout(self.vLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        # menu
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 551, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "nReader"))

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

class ImageWidget(QtWidgets.QGroupBox):
    def __init__(self):
        super(ImageWidget, self).__init__()

        self.setStyleSheet('background-color: #396482;')

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setText('ttestt')
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        #sizePolicy.setHeightForWidth(self.captionLabel.sizePolicy().hasHeightForWidth())
        self.captionLabel.setSizePolicy(sizePolicy)
        self.captionLabel.setScaledContents(True)
        self.captionLabel.setText('Kiritan no Tadashii Shitsuke-kata')
        self.captionLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignCenter)
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

    def setupImage(self, img_url):
        #img_url = 'https://t.nhentai.net/galleries/1594289/thumb.jpg'
        img_data = requests.get(img_url)
        pix = QtGui.QPixmap()
        pix.loadFromData(img_data.content)
        w = 250
        self.imageLabel.setPixmap(pix.scaledToWidth(w))


