from threading import Thread

from PyQt5.QtCore import pyqtSignal, QThread

from Downloader import DownloadByNum
from queue import Queue
import time


class TutorialThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        pass

    def run(self):
        for i in range(1, 11):
            self.push_data.emit(str(i))

class DownloadHttpList(QThread):
    push_data = pyqtSignal(str)

    def __init__(self):
        super(DownloadHttpList, self).__init__()
        self.num = ''
        self.http_list = Queue()
        self.download_max_num = 1
        self.download_running = False
        self.download_thread = TutorialThread()

    def _download(self):
        while not self.http_list.empty():
            self.download_running = True
            num = self.http_list.get()
            # print(f'{self.http_list.qsize()} 本書 等待下載中...')
            self.push_data.emit(f'{self.http_list.qsize()} 本書 等待下載中...')
            d = DownloadByNum(num)
            d.downloadAll()
            self.download_running = False

    def _startDownload(self):
        if not self.download_running:
                t = Thread(target=self._download())
                t.start()

    def setDownloadMaxNum(self, num):
        self.download_max_num = num

    def pushHttp(self, num):
        self.http_list.put(num)
        if not self.http_list.empty():
            self._startDownload()
        # print(f'{self.http_list.qsize()} 本書 等待下載中...')
        self.push_data.emit(f'{self.http_list.qsize()} 本書 等待下載中...')
        self.download_thread.start()
        # self.push_data.emit('test?')

    def run(self, priority=None):
        t = Thread(target=self.pushHttp, args=(self.num,))
        t.start()
