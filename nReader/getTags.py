import re
from queue import Queue
from functools import reduce
from threading import Thread

from requests_html import HTMLSession

class NormalManager:
    def __init__(self, url):
        self.url = url
        self.data_url = []
        self.tags_number_list = []
        self.tags_name_list = []
        self.tags_list = []  # [[{number_set}, {name_set}], ...]

    def getData(self):
        session = HTMLSession()
        result = session.get(self.url)

        # put thumb url into queue
        a = result.html.find('a.cover', first=False)
        self.data_url = ['https://nhentai.net' + url.links.pop() for url in a]

        # get list of tag number set
        div = result.html.find('div.gallery', first=False)
        tag_str = [tag.attrs['data-tags'] for tag in div]
        self.tags_number_list = [set(number.split(' ')) for number in tag_str]

        # get list of tag name set
        for url in self.data_url:
            print(url)
            g = GalleryManager(url)
            g.getData()
            self.tags_name_list.append(g.tags_set)

        # zip number and tag into tag list
        self.tags_list = [list(data) for data in zip(self.tags_number_list, self.tags_name_list)]



class GalleryManager:
    def __init__(self, url):
        self.url = url
        self.tags_set = set()

    def getData(self):
        session = HTMLSession()
        try:
            result = session.get(self.url)
            div = result.html.find('span.tags')
            self.tags_set = {element for d in div for element in
                              list(filter(lambda x: x != '', re.split(r' \((\d*,?)*\)', d.text)))}
        except Exception as e:
            print(f'error: {e}')
        finally:
            session.close()

def intersection(list):
    size = len(list)
    for i in range(size):
        main_set = list[i]
        if i == size-1:
            if len(main_set) == 1:
                return main_set
            return set()
        for j in range(i + 1, size):
            intersection_set = main_set & list[j]
            if len(intersection_set) == 1:
                return intersection_set
            main_set = intersection_set


if __name__ == '__main__':
    n = NormalManager('https://nhentai.net/language/translated/')
    n.getData()

    number_tuple, tags_tuple = zip(*n.tags_list)
    number_list, tags_list = list(number_tuple), list(tags_tuple)
    if len(number_list) == len(tags_list):
        size = len(number_list)
        for index in range(size):
            number_intersection_set = intersection(number_list[index:])
            tags_intersection_set = intersection(tags_list[index:])
            print(f'{number_intersection_set}: {tags_intersection_set}')
            number_list = list(map(lambda x: x ^ number_intersection_set if x else x, number_list))
            tags_list = list(map(lambda x: x ^ tags_intersection_set if x else x, tags_list))
    else:
        print('data error!')



