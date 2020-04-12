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
            image_widget = ImageWidget(url=self.manager.gallery_url[index],
                                               image_path=f'./icon/{self.manager.language[index]}.png',
                                               caption=self.manager.caption[index])
            image_widget.groupClickSignal.connect(self.on_image_widget_clicked)
            image_widget.downloadClickSignal.connect(self.on_download_button_clicked)
            self.img_widget.append(image_widget)
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

    def on_image_widget_clicked(self, url):
        print(f'load: {url}')
        # disconnect

    def on_download_button_clicked(self, url):
        print(f'download: {url}')
        # disconnect



class GalleryPage:
    def __init__(self):
        self.ui = GalleryUi()
        self.manager = GalleryManager()


class BookPage:
    def __init__(self):
        self.ui = BookUi()
        self.manager = BookManager()


class ImageWidget(QtWidgets.QGroupBox):
    groupClickSignal = QtCore.pyqtSignal(str)
    downloadClickSignal = QtCore.pyqtSignal(str)
    def __init__(self, url='', image_path='./icon/Japanese.png', caption=''):
        super(ImageWidget, self).__init__()
        self.url = url
        # 主要框架
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet('background-color: #404040;')

        # 垂直布局
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.verticalLayout)

        # 圖片視窗
        self.imageLabel = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.imageLabel)

        # 水平布局
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)

        # 語言圖示
        self.languageLabel = QtWidgets.QLabel()
        self.languageLabel.setStyleSheet('padding: 0px;')
        pixmap = QtGui.QPixmap(image_path)
        self.languageLabel.setPixmap(pixmap.scaledToHeight(20))
        self.horizontalLayout.addWidget(self.languageLabel)

        # 標題
        self.captionLabel = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        self.captionLabel.setSizePolicy(sizePolicy)
        self.captionLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignCenter)
        self.captionLabel.setScaledContents(True)
        self.captionLabel.setWordWrap(True)
        self.captionLabel.setText(caption)
        self.horizontalLayout.addWidget(self.captionLabel)

        # 下載按鈕
        self.downloadButton = QtWidgets.QPushButton()
        self.downloadButton.setIcon(QtGui.QIcon(QtGui.QPixmap('./icon/download_light.png')))
        self.downloadButton.clicked.connect(self.downloadClicked)
        self.horizontalLayout.addWidget(self.downloadButton)

        # 水平布局分配
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 20)
        self.horizontalLayout.setStretch(2, 1)

    def setupImage(self, img_url):
        img_data = requests.get(img_url)
        pix = QtGui.QPixmap()
        pix.loadFromData(img_data.content)
        w = 250
        self.imageLabel.setPixmap(pix.scaledToWidth(w))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.groupClickSignal.emit(self.url)

    def downloadClicked(self):
        self.downloadClickSignal.emit(self.url)

if __name__ == '__main__':
    import  sys
    app = QtWidgets.QApplication([])
    n = NormalPage()
    n.show()
    n.setUrl('https://nhentai.net/')
    n.setup()
    sys.exit(app.exec_())