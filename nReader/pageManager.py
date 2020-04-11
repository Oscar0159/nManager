import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from ui.PageUi import NormalUi, GalleryUi, BookUi
from htmManager import NormalManager, GalleryManager, BookManager


class NormalPage:
    def __init__(self):
        self.ui = NormalUi()
        self.manager = NormalManager()


class GalleryPage:
    def __init__(self):
        self.ui = GalleryUi()
        self.manager = GalleryManager()


class BookPage:
    def __init__(self):
        self.ui = BookUi()
        self.manager = BookManager()


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