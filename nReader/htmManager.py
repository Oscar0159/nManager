from queue import Queue

from requests_html import HTMLSession


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

            # for key, value in self.pagination.items():
            #     print(f'{key} : {value}')
        except Exception as e:
            print(f'error: {e}')
        finally:
            session.close()

    def addThumbnail(self):
        for url in self.thumbnail:
            pass

    def addPagination(self):
        for page in self.pagination['page'][::-1]:
            print(f'{page.text} : {page.attrs["href"]}')
            # url_button = UrlButton(text=f'{page.text}', url=f'{page.attrs["href"]}')
            # self.ui.pagination_hlayout.insertWidget(index=2, widget=url_button)


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
        self.pages = 0
        self.image_queue = Queue()  # 所有原圖

    def getData(self):
        session = HTMLSession()
        try:
            result = session.get(self.url)
            gallery_id = result.html.search('"media_id":"{}"')[0]
            self.pages = result.html.search('<div>{} pages</div>')[0]

            thumbnail = [element.attrs['data-src']
                         for element in result.html.find('div#thumbnail-container img.lazyload', first=False)]
            image_format = [url.split('/')[-1].split('.')[1] for url in thumbnail]
            image = [f'https://i.nhentai.net/galleries/{gallery_id}/{index+1}.{format_}'
                     for index, format_ in enumerate(image_format)]
            [self.image_queue.put(url) for url in image]

            while not self.image_queue.empty():
                print(self.image_queue.get())
        except Exception as e:
            print(f'error: {e}')
        finally:
            session.close()


if __name__ == '__main__':
    n = NormalManager()
    n.setUrl('https://nhentai.net/')
    n.getData()
    n.addPagination()