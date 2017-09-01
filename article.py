from markov import markov
from uuid import uuid4
import hashlib
class article:
    def __init__(self, d = None):
        if d:
            self.__dict__ = d
            return
        self.headline = markov()
        image_urls = image.get_image_urls(self.headline)
        self.guid = uuid4().hex
        self.images = []
        for _ in image_urls:
            img = image(_, self.guid)
            self.images.append(('./static/images/{}/{}'.format(self.guid,img.filename), img.caption))
        return None

class image:
    def __init__(self, url, guid):
        self.filename = ''
        self.article = guid
        self.download_image(url)
        self.caption = self.get_caption(url)

    def download_image(self, url):
        import urllib.request
        import os
        import http
        path = os.getcwd()
        directory = 'static/images/{}'.format(self.article)
        os.makedirs(directory, exist_ok=True)
        os.chdir(directory)
        self.filename = 'image{:08d}'.format(len(os.listdir()))
        try:
            urllib.request.urlretrieve(url, self.filename)
        except urllib.error.HTTPError:
            print(url)
        except http.client.RemoteDisconnected:
            pass
        except ValueError:
            pass
        except:
            pass
        os.chdir(path)
        return
    
    @staticmethod
    def get_image_urls(line, limit = 10):
        import time
        import urllib
        from selenium import webdriver
        from pyvirtualdisplay import Display
        line = urllib.parse.quote_plus(line)
        query = 'http:/www.google.com/search?tbm=isch&tbs=sur:fmc&*&q={}'.format(line)
        display = Display(visible=0, size=(800,600))
        display.start()
        browser = webdriver.Chrome()
        browser.get(query)
        time.sleep(1)
        elems = [_.get_attribute('href') for _ in browser.find_elements_by_class_name('rg_l')] # TODO: get link to page as well as direct link
        #_ = urllib.parse.unquote_plus(_)
        return list(set([urllib.parse.unquote(_[_.index('=') + 1:_.index('&')]) for _ in elems]))[:limit]
        elems = [_.get_attribute('href') for _ in browser.find_elements_by_class_name('rg_l')]
        elems = list(set(elems))[:limit]
        return list(map(image.get_image_from_link, elems))
    
    @staticmethod
    def get_caption(url = 'https://static.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg'):
        import urllib.request
        import http
        from bs4 import BeautifulSoup
        query = 'https://www.google.com/searchbyimage?image_url={}'.format(urllib.parse.quote(url, safe=''))
        headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0' }
        req = urllib.request.Request(query, None, headers)
        with urllib.request.urlopen(req) as response:
            bs = BeautifulSoup(response.read(), 'html.parser')
            try:
                return bs.find_all('a', {'class': '_gUb'})[0].get_text(' ', strip = True)
            except IndexError:
                return ''
       
    """@staticmethod
    def get_image_urls(line, limit = 5):
        import urllib.request
        from bs4 import BeautifulSoup
        query = 'http://www.google.com/search?tbm=isch&tbs=sur:fmc&*&q={}'.format(urllib.parse.quote_plus(line, safe='')) 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0'}
        req = urllib.request.Request(query, None, headers)
        elems = []
        unquoted = []
        with urllib.request.urlopen(req) as response:
            bs = BeautifulSoup(response.read(), 'html.parser')
            elems = bs.find_all('a', {'class': 'rg_l'})
            for _ in elems:
                print(_)
                unquoted.append(urllib.parse.unquote_plus(_.get('href')))
        return unquoted"""

    @staticmethod
    def get_image_from_link(s):
        import urllib
        url = urllib.parse.urlparse(s)
        query = url.query
        qs = urllib.parse.parse_qs(query)
        imgurls = qs.get('imgurl')
        imgurl = next(iter(imgurls), None)
        unquoted = urllib.parse.unquote_plus(imgurl)
        return unquoted
