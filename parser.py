from PIL import Image
import io
from requests import get
from selenium import webdriver
from time import sleep


# Путь к драйверу для selenium
DRIVER_PATH = 'C:\Home\Projects\CODE\CV projects\police\driver\chromedriver.exe'

# Примерный лимит картинок
IMAGES_LIMIT = 500
wd = webdriver.Chrome(executable_path=DRIVER_PATH)

# Ссылка на страницу гугла с картинками
search_url = 'https://www.google.com/search?q=' \
             '%D0%BF%D0%BE%D0%BB%D0%B8%D1%86%D0%B5%D0%B9%D1%81%D0%BA%D0%B8%D0%B9+' \
             '%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C+' \
             '%D1%80%D0%BE%D1%81%D1%81%D0%B8%D1%8F&sxsrf=' \
             'ALeKk028LL0QShdNU4eQV87B7y0IvCSxqw:1625677596089&source=l' \
             'nms&tbm=isch&sa=X&ved=2ahUKEwiF74j9uNHxAhVktIsKHZgMDLIQ_AUoAXoECAEQAw&biw=1536&bih=722'

wd.get(search_url)
img_urls = []
while IMAGES_LIMIT > len(img_urls):
    results = wd.find_elements_by_css_selector('img.rg_i')
    img_urls += results
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(len(img_urls))

# Путь к папке с изображениями
IMAGE_PATH = 'C:\Home\Projects\CODE\CV projects\police\images\police\\'
name = 0
print(len(img_urls))
i = 0
for img in img_urls:
    try:
        img.click()
        print(img.get_attribute('alt'))
        sleep(2)
        i += 1
        image = wd.find_elements_by_class_name('n3VNCb')
        print(i)
        for lbl in range(len(image)):
            src = image[lbl].get_attribute('src')
            if src[:3] == 'htt':
                break
        image_data = get(src).content
        image_file = io.BytesIO(image_data)
        image2save = Image.open(image_file).convert('RGB')
        image2save.save(IMAGE_PATH + str(name) + '.jpg', 'JPEG', quality=85)
        img_urls.append(src)
        name += 1
    except Exception:
        continue




print(img_urls)
