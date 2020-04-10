from queue import Queue

from requests_html import HTMLSession

def pt(data):
    print(f'{type(data)} : {data}')

class HtmlManager:
    def __init__(self):
        self.url = ''

    def setUrl(self, url):
        self.url = url

    def getData(self):
        pass


class NormalManager(HtmlManager):
    def __init__(self):
        super().__init__()
        self.thumbnail = []  # 所有縮圖
        self.pagination = {}

    def getData(self):
        session = HTMLSession()
        try:
            result = session.get(self.url)
            self.thumbnail = [element.attrs['data-src'] for element in result.html.find('img.lazyload', first=False)]

            keys = ['first', 'previous', 'page', 'current', 'next', 'last']
            values = [result.html.find(f'a.{key}', first=False) for key in keys]
            self.pagination = dict(zip(keys, values))

            for key, value in self.pagination.items():
                print(f'{key} : {value}')
        except Exception as e:
            print(f'error: {e}')
        finally:
            session.close()


class GalleryManager(HtmlManager):
    def __init__(self):
        super().__init__()
        self.heading = []  # 標題
        self.info = {}  # 標籤, 作者, 語言...
        self.thumbnail = []  # 所有縮圖
        self.related = []  # 相關本子

    def getData(self):
        session = HTMLSession()
        try:
            result = session.get(self.url)
            keys = ['h1', 'h2']
            self.heading = [result.html.find(f'div#info {key}', first=True).text for key in keys]

            keys = ['Parodies', 'Characters', 'Tags', 'Artists', 'Groups', 'Languages', 'Categories']
            section = result.html.find('div.tag-container span.tags', first=False)
            values = [element.find('a.tag', first=False) for element in section]
            self.info = dict(zip(keys, values))

            self.thumbnail = [element.attrs['data-src']
                              for element in result.html.find('div#thumbnail-container img.lazyload', first=False)]

            self.related = [element.attrs['data-src']
                            for element in result.html.find('div#related-container img.lazyload', first=False)]
        except Exception as e:
            print(f'error: {e}')
        finally:
            session.close()


class BookManager(HtmlManager):
    def __init__(self):
        super().__init__()
        self.gallery_url = 'https://i.nhentai.net/galleries/'
        self.pages = 0
        self.gallery_id = ''
        self.image_queue = Queue()  # 所有原圖

    def getData(self):
        session = HTMLSession()
        try:
            result = session.get(self.url)
            self.gallery_id = result.html.search('"media_id":"{}"')[0]
            self.pages = result.html.search('<div>{} pages</div>')[0]

            thumbnail = [element.attrs['data-src']
                         for element in result.html.find('div#thumbnail-container img.lazyload', first=False)]
            image_format = [url.split('/')[-1].split('.')[1] for url in thumbnail]
            image = [f'{self.gallery_url + self.gallery_id}/{index+1}.{format_}'
                     for index, format_ in enumerate(image_format)]
            [self.image_queue.put(url) for url in image]

            while not self.image_queue.empty():
                print(self.image_queue.get())
        except Exception as e:
            print(f'error: {e}')
        finally:
            session.close()


if __name__ == '__main__':
    n = BookManager()
    n.setUrl('https://nhentai.net/g/299015/')
    n.getData()