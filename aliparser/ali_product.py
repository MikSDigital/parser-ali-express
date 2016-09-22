from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import re


class AliProduct():
    def __init__(self, product_url):
        try:
            html = urlopen(product_url)
        except HTTPError as e:
            print(e)
        try:
            self.bs_obj = BeautifulSoup(html, 'html5lib')
        except AttributeError as e:
            print(e)

    def get_title(self):
        title = self.bs_obj.find('h1', {'class':'product-name'})
        return title.get_text()

    def get_price(self):
        price = self.bs_obj.find('span', {'id':'j-sku-price'})
        return '$' + price.get_text()

    def get_discount_price(self):
        price = self.bs_obj.find('span', {'id':'j-sku-discount-price'})

        if price is not None:
            return '$' + price.get_text()
        else:
            return ' '

    def get_options(self):
        """
        options = [
            {'Color: ': colors},
            {'Size: ': sizes}
        ]
        """
        properties = self.bs_obj.find('div', {'id':'j-product-info-sku'})\
            .findAll('dl', {'class':'p-property-item'})
        options = []
        for pr in properties:
            k = pr.find('dt').get_text()
            tss =[]
            ts = pr.dd.ul.findAll('li')
            for t in ts:
                if t.a.get('title') is not None:
                    op = t.a.get('title')
                    option_name = str(op)
                    tss.append(option_name)
                else:
                    op = t.a.find('span').get_text()
                    tss.append(op)
            l_options = {k: tss}
            options.append(l_options)
        return options

    def get_specifics(self):
        spec = []
        for specific in self.bs_obj.findAll(
            'li',
            id=re.compile('(product\-prop\-)[0-9]+')
        ):
            k = specific.find(
                'span',
                {'class':'propery-title'}
            ).get_text() + " "
            t = specific.find(
                'span',
                {'class': 'propery-des'}
            ).get_text()
            d = {k: t}
            spec.append(d)
        return spec

    def get_packaging_details(self):
        pack = []
        for package in self.bs_obj.find(
            'ul',
            {'class': 'product-packaging-list'}
        ).findAll(
            'li',
            {'class':'packaging-item'}
        ):
            k = package.find(
                'span',
                {'class': 'packaging-title'}
            ).get_text()
            t = package.find(
                'span',
                {'class': 'packaging-des'}
            ).get_text().rstrip()
            d = {k:t}
            pack.append(d)
        return pack

    def get_image_page(self):
        page_url = self.bs_obj.find(
            'div',
            {'id': 'j-detail-gallery-main'}
        ).find(
            'a',
            {'class': 'ui-image-viewer-thumb-frame'}
        ).attrs['href']
        return 'https:' + page_url

    def get_images_url(self, images_page):
        html = urlopen(images_page)
        bs_obj = BeautifulSoup(html, 'html.parser')
        imgs = []
        for image in bs_obj.find(
            'div',
            {'id': 'change-600-layout'}
        ).findAll('img'):
            image_url = str(image.get('src'))
            imgs.append(image_url)
        return imgs

    def get_category(self):
        cat = self.bs_obj.find(
            'div',
            {'class': 'breadcrumb-layout'}
        ).find(
            'b'
        ).get_text()
        return cat
