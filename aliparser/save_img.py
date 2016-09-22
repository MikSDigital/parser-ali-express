import os
from urllib.request import urlretrieve
from urllib.error import ContentTooShortError


class SaveImg():
    def __init__(self, new_dir_name, images_url):
        os.chdir('images')
        os.mkdir(str(new_dir_name))
        os.chdir(str(new_dir_name))

        count = 1
        for img in images_url:
            img_name = str(count) + '.jpg'
            try:
                urlretrieve(img, img_name)
                count += 1
            except ContentTooShortError as e:
                print(e)
                continue

        os.chdir('..')
        os.chdir('..')
