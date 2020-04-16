from queue import Queue

from requests_html import HTMLSession

NHENTAI = 'https://nhentai.net'

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
        self.gallery_url = []
        self.thumbnail = []  # 所有縮圖
        self.pagination = {}
        self.caption = []
        self.language = []

    def getData(self):
        session = HTMLSession()
        try:
            result = session.get(self.url)
            # self.gallery_url
            self.gallery_url = [NHENTAI + url.links.pop() for url in result.html.find('a.cover', first=False)]

            # self.thumbnail
            self.thumbnail = [element.attrs['data-src'] for element in result.html.find('img.lazyload', first=False)]

            # self.pagination
            keys = ['first', 'previous', 'current', 'next', 'last']
            values = ['https://nhentai.net/' + result.html.find(f'a.{key}', first=True).links.pop()
                      if result.html.find(f'a.{key}') else '' for key in keys]
            self.pagination = dict(zip(keys, values))

            # self.pagination add 'page'
            self.pagination['page'] = result.html.find('a.page', first=False)

            # self.caption
            self.caption = [div.text for div in result.html.find('div.caption', first=False)]

            # self.language
            div = result.html.find('div.gallery', first=False)
            tag_str = [tag.attrs['data-tags'] for tag in div]
            tags_number_list = [set(number.split(' ')) for number in tag_str]
            for number_set in tags_number_list:
                if '12227' in number_set:
                    self.language.append('English')
                elif '29963' in number_set:
                    self.language.append('Chinese')
                else:
                    self.language.append('Japanese')


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

            self.cover = result.html.find('div#cover img', first=True).attrs['data-src']

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