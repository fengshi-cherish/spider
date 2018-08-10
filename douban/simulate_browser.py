import os
from selenium import webdriver
from pyquery import PyQuery as pq
driver = webdriver.Chrome()

class Model(object):
    """
    基类, 用来显示类的信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{}     \n{}>'.format(name, '\n  '.join(properties))
        return s

class RecommendItems(Model):
    def __init__(self):
        self.title = ''
        self.cover_url = ''
        self.abstract = ''


def cache_url(url):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'cached_zh'
    filename = url.rsplit('/')[-2] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:

        if not os.path.exists(folder):
            os.makedirs(folder)

        driver.get(url)

        with open(path, 'wb') as f:
            f.write(driver.page_source.encode())
        content = driver.page_source
        return content


def item_from_div(div):
    e = pq(div)
    m = RecommendItem()
    m.abstract = e(".post_box_main .text").text()
    m.name = e(".title_box a").text()
    m.cover_url = e('.post_box_img img').attr('src')
    return m

def item_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    page = cache_url(url)
    e = pq(page)
    items = e(".post_box")
    return [item_from_div(i) for i in items]

def main():
    items = item_from_url('https://zhizhizhi.com/gn/1/')
    for i in range(0, 10):
        items = item_from_url("https://zhizhizhi.com/gn/{}/".format(i))
        print(items)
    driver.close()

if __name__ == '__main__':
    main()
