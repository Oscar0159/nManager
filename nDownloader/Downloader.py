import requests
from requests_html import HTMLSession
import os
import time
import re
from threading import Thread
from queue import Queue

Nhentai = 'https://nhentai.net/g/'
iNhentai = 'https://i.nhentai.net/galleries/'   # 原始圖檔目錄
tNhentai = 'https://t.nhentai.net/galleries/'   # 預覽圖檔目錄


def excute_time_decorator(func):
    def excuteTime(*args):
        start = time.time()
        func(*args)
        end = time.time()
        cost = round(end - start)
        print(f'總時間: {cost} 秒')
    return excuteTime


class Downloader:

    def __init__(self, url):
        self._thread_num = 10
        self._http_url = url
        self._save_dir = os.getcwd() + os.sep + 'download'
        self._download_queue = Queue()

    def setThread(self, num):
        self._thread_num = num

    def setDir(self, path):
        self._save_dir = path

    def _getData(self):
        pass

    def _createFolder(self):
        pass

    def _saveImageUrl(self):
        pass

    def _downloadImage(self):
        pass


class DownloadByNum(Downloader):

    def __init__(self, num):
        super().__init__(Nhentai + str(num) + '/')
        self._page_num = 0
        self._serial_num = num
        self._gallery_id = ''

    def _getData(self):
        try:
            session = HTMLSession()
            result = session.get(self._http_url)  # 使用GET取得網頁資料
            self._gallery_id = result.html.search('"media_id":"{}"')[0]  # 取得畫廊編號
            self._page_num = result.html.search('<div>{} pages</div>')[0]  # 取得頁數
            img_list = result.html.find('div.container#thumbnail-container div a img.lazyload', first=False)
            for element_img in img_list:    #儲存圖片下載位置
                substr = element_img.attrs['data-src'].split('/')[-1].split('.')
                img_index = substr[0][:-1]
                img_format = substr[1]
                image_url = iNhentai + self._gallery_id + '/' + img_index + '.' + img_format
                self._download_queue.put(image_url, block=False)
        except Exception as e:
            print(f'取得資料錯誤 ： {e}')
            time.sleep(0.5)

    def _createFolder(self):
        try:
            if (not os.path.exists(self._save_dir)):  # 建立下載目錄
                os.mkdir(self._save_dir)

            if (os.path.exists(self._save_dir)):  # 下載目錄存在
                self._save_path = self._save_dir + os.sep + str(self._serial_num)
                if (not os.path.exists(self._save_path)):  # 建立下載目標資料夾
                    os.mkdir(self._save_path)
                else:  # 下載目標資料夾存在 -> 下載缺少的圖片
                    pass
        except Exception as e:
            print(f'創建資料夾錯誤 : {e}')
        else:
            print(f'創建資料夾 : {self._serial_num}  位置:{self._save_path}')

    def _saveImageUrl(self):
        pass
        # for i in range(1, int(self._page_num) + 1):
        #     image_url = iNhentai + self._gallery_id + '/' + str(i) + '.jpg'
        #     self._download_queue.put(image_url, block=False)

    def _downloadImage(self):
        while not self._download_queue.empty():
            image_url = self._download_queue.get()
            file_name = image_url.split('/')[-1]
            #print(f'{file_name} 開始下載')
            try:
                img_data = requests.get(image_url).content
                with open(f'{self._save_path}{os.sep}{file_name}', 'wb') as img:
                    img.write(img_data)
            except Exception as e:
                print(f'取得資料錯誤：{e} ')
                time.sleep(0.5)

    @excute_time_decorator
    def downloadAll(self):  # 多線程執行
        try:
            self._createFolder()

            self._getData()

            threads = []
            for i in range(self._thread_num):
                t = Thread(target=self._downloadImage)
                t.setDaemon(True)
                t.start()
                threads.append(t)

            for t in threads:
                t.join()
        except Exception as e:
            print(f'下載錯誤 : {e}')

    def downloadRange(self, start, end):  # 多線程執行
        self._createFolder()
        self._getData()
        self._saveImageUrl()

    def downloadSelect(self):  # 多線程執行
        pass


class DownloadByUrl(Downloader):
        pass


class DownloadBySearch(Downloader):
        pass


class DownloadBySearchUrl(Downloader):
        pass
