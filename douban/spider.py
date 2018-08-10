import os
import requests
from pyquery import PyQuery as pq

class Model(object):
    def __repr__(self):
        """
        打印基类信息
        """
        name = self.__class__.__name__
        properties = ('{} = ({})'.format(k,v) for k,v in self.__dict__.items())
        s = '\n<{}    \n    {}>'.format(name, '\n    '.join(properties))
        return s


class Movie(Model):
    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0



def movie_from_url(url):
    """
    从url中下载网页并且解析所有的电影
    """
    """
    只请求一次下载
    """
    page = cache_url(url)
    e = pq(page)
    items = e('.item')
    movies = [movie_from_div(i) for i in items]
    return movies



def movie_from_div(div):
    e = pq(div)
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()
    return m

def cache_url(url):

    folder = 'cache'
    filename = url.split('=')[-1] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)

        headers = {
          'user-agent':'''Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0)
           Gecko/20100101 Firefox/'''
        }

        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content

def download_img(url):
    folder = "img"
    filename = url.split('/')[-1]
    path = os.path.join(folder, filename)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(path):
            return


    headers = {
      'user-agent':'''Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0)
       Gecko/20100101 Firefox/'''
    }

    r = requests.get(url, headers)
    with open(path, 'wb') as f:
        f.write(r.content)



def main():
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies = movie_from_url(url)
        #print('top250 movies', movies)
        [download_img(m.cover_url) for m in movies]

if __name__ == '__main__':
    main()
