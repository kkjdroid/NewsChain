from markov import markov
from datetime import datetime
import hashlib
class article:
    def __init__(self, d = None):
        if d:
            self.__dict__ = d
            return
        self.headline = markov()
        image_urls = image.get_image_urls(self.headline)
        self.guid = hashlib.md5(repr(datetime.now()).encode('utf-8')).hexdigest()
        self.images = []
        for _ in image_urls:
            img = image(_, self.guid)
            self.images.append(('./static/images/{}/{}'.format(self.guid,img.filename), img.caption))
        return

class image:
    def __init__(self, url, guid):
        self.filename = ''
        self.article = guid
        self.download_image(url)
        self.caption = self.get_caption(url)

    def download_image(self, url):
        import urllib.request
        import os
        os.chdir('static/images')
        if not os.path.exists(self.article):
            os.makedirs(self.article)
        os.chdir(self.article)
        self.filename = 'image{:08d}.format(len(os.listdir()))'
        try:
            urllib.request.urlretrieve(url, self.filename)
        except urllib.error.HTTPError:
            print(url)
        except http.client.RemoteDisconnected:
            pass
        print(self.filename)
        os.chdir('../../..')
        return
    
    @staticmethod
    def get_caption(url):
        import time
        import urllib
        from selenium import webdriver
        import selenium
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(800,600))
        display.start()
        browser = webdriver.Chrome()
        query = 'https://www.google.com/searchbyimage?image_url={}'.format(urllib.parse.quote(url, safe=""))
        print(query)
        browser.get(query)
        time.sleep(1)
        caption = ''
        try:
            caption = browser.find_element_by_class_name('_gUb').text
        except selenium.common.exceptions.NoSuchElementException:
            print('None')
        return caption
            
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
        elems = [_.get_attribute('href') for _ in browser.find_elements_by_class_name('rg_l')]
        #_ = urllib.parse.unquote_plus(_)
        return list(set([urllib.parse.unquote(_[_.index('=') + 1:_.index('&')]) for _ in elems]))[:limit]
