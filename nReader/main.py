import time
from threading import Thread
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from queue import Queue

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from requests_html import HTMLSession

iNhentai = 'https://i.nhentai.net/galleries/'   # 原始圖檔目錄

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 變數元素
        self._thread_num = 10
        self.num = ''
        self.gallery_id = ''
        self.page_num = ''
        self.download_queue = Queue()
        self.http_url = ''
        self.labelList = []


    def setupUi(self):
        # QLineEdit
        self.NumLineEdit = QtWidgets.QLineEdit()
        self.NumLineEdit.setObjectName('NumLineEdit')
        self.NumLineEdit.setValidator(QIntValidator(1, 999999))
        self.NumLineEdit.setPlaceholderText('xxxxxx')
        self.NumLineEdit.setGeometry(0, 0, 151, 28)
        self.NumLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.NumLineEdit.setStyleSheet('color: rgb(255, 255, 255);\n'
                                       'padding: 5px;\n'
                                       'font-size: 24px;\n'
                                       'border-width: 1px;\n'
                                       'border-color: #76797C;\n'
                                       'border-style: solid;\n'
                                       'border-radius: 5px;\n'
                                       'outline: none;')

        # QFormLayout
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # QGroupBox
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.setLayout(self.formLayout)

        # QScrollArea
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumWidth(400)
        self.scrollArea.setMinimumHeight(600)
        self.scrollArea.setStyleSheet('border-width: 1px;\n'
                                      'border-color: #76797C;\n'
                                      'border-style: solid;\n'
                                      'padding: 5px;\n'
                                      'border-radius: 5px;\n'
                                      'outline: none;')


        # QPushButton
        self.downloadButton = QtWidgets.QPushButton()
        pixmap = QtGui.QPixmap('download.ico')
        icon = QtGui.QIcon(pixmap)
        self.downloadButton.setIcon(icon)
        self.downloadButton.setStyleSheet('border-width: 1px;\n'
                                          'border-color: #76797C;\n'
                                          'border-style: solid;\n'
                                          'padding: 5px;\n'
                                          'border-radius: 5px;\n'
                                          'outline: none;\n'
                                          'height: 50px;\n'
                                          'width: 50px;')
        self.downloadButton.clicked.connect(self.msg)
        self.buttonForm = QtWidgets.QLayout()

        # QVBoxLayout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.NumLineEdit)
        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.downloadButton)

        # MainWidget
        self.resize(600, 900)
        self.setWindowTitle('nReader')
        self.setLayout(self.layout)
        self.setStyleSheet('background-color: #323232')
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowOpacity(0.95)
        # self.setAttribute(Qt.WA_NoSystemBackground, True)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.resized.connect(self.say)

        # signal connect
        self.NumLineEdit.returnPressed.connect(self.startDisplay)

    def paintEvent(self, QPaintEvent):
        #print('paintEvent')
        pass

    def resizeEvent(self, QResizeEvent):
        #print(self.groupBox.size())
        self.resizeImage()

    def resizeImage(self):
        for i in self.labelList:
            print(self.scrollArea.size())
            #QtWidgets.QLabel.resize(self.scrollArea.size())
            i.resize(self.scrollArea.size())

    def startDisplay(self):
        self.num = self.NumLineEdit.text()  # 取得編號
        self.NumLineEdit.clear()    # 清除輸入區
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
            self.labelList.append(QtWidgets.QLabel())
            self.labelList[i].setAlignment(QtCore.Qt.AlignCenter)
            self.labelList[i].setScaledContents(True)
            self.formLayout.insertRow(i, self.labelList[i])

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
            piximap = QtGui.QPixmap()
            piximap.loadFromData(img_data.content)
            self.labelList[img_index - 1].setPixmap(piximap)

    def msg(self):
        QtWidgets.QMessageBox.information(self, 'title', 'msg', QtWidgets.QMessageBox.Yes)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWidget()
    widget.setupUi()
    widget.show()

    sys.exit(app.exec_())