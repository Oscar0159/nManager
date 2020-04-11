from queue import Queue
from threading import Thread
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from ui.PageUi import NormalUi, GalleryUi, BookUi
from htmManager import NormalManager, GalleryManager, BookManager


class UrlButton(QtWidgets.QPushButton):
    loadPageSignal = QtCore.pyqtSignal(str)
    def __init__(self, text: str, url: str):
        super(UrlButton, self).__init__(text=text)
        self.url = url

        # self.setProperty('mandatoryField', "True")
        self.clicked.connect(self.onClicked)

    def onClicked(self):
        self.loadPageSignal.emit(self.url)


class NormalPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(NormalPage, self).__init__(parent)
        self.ui = NormalUi()
        self.ui.setupUi(self)
        self.manager = NormalManager()

    def setUrl(self, url):
        self.manager.setUrl(url)

    def setup(self):
        self.manager.getData()
        self.img_widget = []
        self.q = Queue()
        [self.q.put([index, url]) for index, url in enumerate(self.manager.thumbnail)]
        for index in range(self.q.qsize()):
            self.img_widget.append(ImageWidget())
            self.ui.flow_layout.addWidget(self.img_widget[index])

        for _ in range(10):
            t = Thread(target=self.loadImage)
            t.setDaemon(True)
            t.start()

        for page_element in self.manager.pagination['page'][::-1]:
            url_button = UrlButton(page_element.text, 'https://nhentai.net/' + page_element.links.pop())
            url_button.loadPageSignal.connect(self.loadPage)
            self.ui.pagination_hlayout.insertWidget(2, url_button)

    def loadImage(self):
        while not self.q.empty():
            index, url = self.q.get()
            self.img_widget[index].setupImage(url)

    def loadPage(self, url):
        self.ui = NormalUi()
        self.ui.setupUi(self)
        self.manager = NormalManager()
        self.manager.setUrl(url)
        print(url)
        self.setup()



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

        self.setStyleSheet('background-color: #404040;')

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


if __name__ == '__main__':
    import  sys
    app = QtWidgets.QApplication([])
    n = NormalPage()
    n.show()
    n.setUrl('https://nhentai.net/')
    n.setup()
    sys.exit(app.exec_())