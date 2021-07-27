from PIL import Image
import io
from requests import get
from selenium import webdriver
import json
from yaml import load
from os import mkdir


class ImageParser:
    def __init__(self, file):
        f = open(file, 'r', encoding='utf-8')
        self.config = load(f)
        print(self.config)
        DRIVER_PATH = self.config['driver_path']
        self.IMAGES_LIMIT = int(self.config['images_limit'])
        self.wd = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.TYPES = self.config['types']
        self.images_urls = set()
        self.IMAGE_PATH = self.config['images_path']
        self.ENGINES = self.config['search_engines']

    def google_download(self, REQUEST):
        # Ссылка на страницу гугла с картинками
        req = REQUEST.replace(' ', '+')
        search_url = f'https://www.google.com/search?q={req}&tbm=isch&ved=2ahUKEwjB6aLjsvLxAhXUsSoKHZkNDV4Q2-' \
                     f'cCegQIABAA&oq={req}&gs_lcp=CgNpbWcQA1AAWABgpwtoAHAAeACAAQCIAQCSAQCYAQCqAQtnd3Mtd2l6LWltZw' \
                     f'&sclient=img&ei=yiX3YMHcLNTjqgGZm7TwBQ&bih=722&biw=1536&hl=ru'
        self.wd.get(search_url)
        img_urls = []
        while self.IMAGES_LIMIT > len(img_urls):
            results = self.wd.find_elements_by_css_selector('img.rg_i')
            img_urls += results
            self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(img_urls))

        print(len(img_urls))
        i = 0
        for img in img_urls:
            try:
                img.click()
                print(img.get_attribute('alt'))
                # sleep(1)
                i += 1
                image = self.wd.find_elements_by_class_name('n3VNCb')
                for lbl in range(len(image)):
                    src = image[lbl].get_attribute('src')
                    if src[:3] == 'htt':
                        break
                self.images_urls.add(src)
            except Exception:
                continue

    def yandex_download(self, REQUEST):
        req = REQUEST.replace(' ', '%20')
        search_url = f'https://yandex.ru/images/search?from=tabbar&text={req}'
        self.wd.get(search_url)
        img_urls = []
        i = 0
        while self.IMAGES_LIMIT > i:
            results = self.wd.find_elements_by_css_selector('div.serp-item')
            for im in results:
                data = json.loads(im.get_attribute('data-bem'))['serp-item']['snippet']
                self.images_urls.add(data['url'])
                print(data['title'])
                i += 1
            self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(img_urls))

    def bing_download(self, REQUEST):
        req = REQUEST.replace(' ', '+')
        search_url = f'https://www.bing.com/images/search?q={req}&form=HDRSC2&first=1&tsc=ImageBasicHover'
        self.wd.get(search_url)
        img_urls = []
        i = 0
        while self.IMAGES_LIMIT > i:
            results = self.wd.find_elements_by_css_selector('a.iusc')
            for im in results:
                data = json.loads(im.get_attribute('m'))
                self.images_urls.add(data['purl'])
                print(data['t'])
                i += 1
            self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(len(img_urls))

    def download_image(self, urls, path):
        name = 0
        for url in urls:
            try:
                image_data = get(url).content
                image_file = io.BytesIO(image_data)
                image2save = Image.open(image_file).convert('RGB')
                image2save.save(path + str(name) + '.jpg', 'JPEG', quality=85)
                name += 1
            except Exception:
                continue

    def parse(self):
        for type in self.TYPES:
            path = self.IMAGE_PATH + type + '\\'
            print(path)
            mkdir(path)
            for request in self.config['types'][type]['requests']:
                if 'google' in self.ENGINES:
                    self.google_download(request)
                if 'yandex' in self.ENGINES:
                    self.yandex_download(request)
                if 'bing' in self.ENGINES:
                    self.bing_download(request)
            self.download_image(self.images_urls, path)
            self.images_urls = set()


config_file = 'conf.yaml'
process = ImageParser(config_file)
process.parse()
