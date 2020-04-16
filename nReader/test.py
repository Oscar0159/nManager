import math
import time
import sys
from functools import partial

import aiohttp
from aiohttp import web
import asyncio
import requests
from requests_html import HTMLSession
from threading import Thread, currentThread
from concurrent.futures import ProcessPoolExecutor
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QProgressBar
from quamash import QEventLoop

from ui.testUi import MainWindowUi
from htmManager import NormalManager, GalleryManager, BookManager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowUi()
        self.ui.setup(self)
        self.manager = NormalManager()
        self.manager.setUrl('https://nhentai.net/search/?q=henreader')
        Thread(target=self.manager.getData).start()

    @QtCore.pyqtSlot(str)
    def on_myButton_mySignal(self, data):
        pass


def main():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()