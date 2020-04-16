from queue import Queue
from threading import Thread
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from ui.PageUi import NormalUi, GalleryUi, BookUi, UrlButton
from htmManager import NormalManager, GalleryManager, BookManager


class NormalPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        # add image label
        for index in range(self.q.qsize()):
            image_widget = ImageWidget(url=self.manager.gallery_url[index],
                                       image_path=f'./icon/{self.manager.language[index]}.png',
                                       caption=self.manager.caption[index])
            image_widget.groupClickSignal.connect(self._on_image_widget_clicked)
            image_widget.downloadClickSignal.connect(self._on_download_button_clicked)
            self.img_widget.append(image_widget)
            self.ui.flow_layout.addWidget(self.img_widget[index])

        # load thumbnail image
        for _ in range(10):
            t = Thread(target=self._loadImage)
            t.setDaemon(True)
            t.start()

        # add page button
        for page_element in self.manager.pagination['page'][::-1]:
            url_button = UrlButton(text=page_element.text, url='https://nhentai.net/' + page_element.links.pop(),
                                   icon=QtGui.QIcon())
            url_button.loadPageSignal.connect(self._loadPage)
            self.ui.pagination_hlayout.insertWidget(2, url_button)

        # add first, previous, next, last button url
        url =  self.manager.pagination['first']
        self.ui.first_button.setUrl(url if url else '')
        self.ui.first_button.loadPageSignal.connect(self._loadPage)
        url = self.manager.pagination['previous']
        self.ui.previous_button.setUrl(url if url else '')
        self.ui.previous_button.loadPageSignal.connect(self._loadPage)
        url = self.manager.pagination['next']
        self.ui.next_button.setUrl(url if url else '')
        self.ui.next_button.loadPageSignal.connect(self._loadPage)
        url = self.manager.pagination['last']
        self.ui.last_button.setUrl(url if url else '')
        self.ui.last_button.loadPageSignal.connect(self._loadPage)

    def _loadImage(self):
        while not self.q.empty():
            index, url = self.q.get()
            self.img_widget[index].setupImage(url)

    def _loadPage(self, url):
        if url.strip(' '):
            self.ui = NormalUi()
            self.ui.setupUi(self)
            self.manager = NormalManager()
            self.manager.setUrl(url)
            print(url)
            self.setup()

    def _on_image_widget_clicked(self, url):
        print(f'load: {url}')
        # disconnect

    def _on_download_button_clicked(self, url):
        print(f'download: {url}')
        # disconnect


class GalleryPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(GalleryPage, self).__init__(parent)
        self.ui = GalleryUi()
        self.ui.setupUi(self)
        self.manager = GalleryManager()

    def setUrl(self, url):
        self.manager.setUrl(url)

    def setup(self):
        self.manager.getData()

        # setup cover
        Thread(target=self._setCover).start()

        # setup thumbnail
        self.img_widget = []
        self.q = Queue()
        [self.q.put([index, url]) for index, url in enumerate(self.manager.thumbnail)]
        for index in range(self.q.qsize()):
            image_widget = QtWidgets.QLabel()
            self.img_widget.append(image_widget)
            self.ui.thumbnail_layout.addWidget(self.img_widget[index])

        for _ in range(10):
            t = Thread(target=self._loadImage)
            t.start()

    def _setCover(self):
        head_image = requests.get(self.manager.cover)
        pix = QtGui.QPixmap()
        pix.loadFromData(head_image.content)
        self.ui.cover_image.setPixmap(pix)

    def _loadImage(self):
        while not self.q.empty():
            index, url = self.q.get()
            image = requests.get(url)
            pix = QtGui.QPixmap()
            pix.loadFromData(image.content)
            self.img_widget[index].setPixmap(pix)


class BookPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(BookPage, self).__init__(parent)
        self.ui = BookUi()
        self.ui.setupUi(self)
        self.manager = BookManager()

    def setUrl(self, url):
        self.manager.setUrl(url)

    def setup(self):
        self.manager.getData()


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

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.rect().contains(event.pos()):
            self.groupClickSignal.emit(self.url)

    def downloadClicked(self):
        self.downloadClickSignal.emit(self.url)


if __name__ == '__main__':
    import  sys
    app = QtWidgets.QApplication([])
    n = GalleryPage()
    n.show()
    n.setUrl('https://nhentai.net/g/252213/')
    n.setup()
    sys.exit(app.exec_())