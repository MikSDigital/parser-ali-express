import os
import shutil
import time
from datetime import datetime
from ali_product import AliProduct
from ali_parser import AliParser
import xlwt as x1
from save_img import SaveImg


class AliExport():
    def __init__(self, url_market, save_img):
        self.save_img = save_img
        print('Wait...')
        self.workbook = x1.Workbook()
        self.sheet = self.workbook.add_sheet('AliExpress')
        style = x1.easyxf('font: bold on')
        now = datetime.now()
        file_name = str(now.year)+'-'+str(now.day)+'-'+str(now.month)+'-'+str(now.hour)+'h'+str(now.minute)+'m.xls'

        self.sheet.write(0, 0, '#', style)
        self.sheet.write(0, 1, 'Title', style)
        self.sheet.write(0, 2, 'Category', style)
        self.sheet.write(0, 3, 'Price', style)
        self.sheet.write(0, 4, 'Discount Price', style)
        self.sheet.write(0, 5, 'Options', style)
        self.sheet.write(0, 6, 'Item specifics', style)
        self.sheet.write(0, 7, 'Packaging Details', style)
        self.sheet.write(0, 8, 'Images URL', style)
        self.sheet.write(0, 9, 'Product URL', style)

        if self.save_img:
            if os.path.exists('images'):
                shutil.rmtree('images')
            os.mkdir('images')

        if not os.path.exists('reports'):
            os.mkdir('reports')

        self._field_cells(url_market)

        os.chdir('reports')
        self.workbook.save(file_name)
        os.chdir('..')


    def _field_cells(self, url_market):
        ali_parser = AliParser(url_market)
        product_url = ali_parser.return_pages()
        print('Total Products', len(product_url), '\n')

        for n in range(0, len(product_url)):
            row = n + 1
            product = AliProduct(product_url[n])

            self.sheet.write(row, 0, row)
            self.sheet.write(row, 1, product.get_title())
            self.sheet.write(row, 2, product.get_category())
            self.sheet.write(row, 3, product.get_price())
            self.sheet.write(row, 4, product.get_discount_price())
            self.sheet.write(row, 5, self._get_options(product))
            self.sheet.write(row, 6, self._get_spec(product))
            self.sheet.write(row, 7, self._get_details(product))
            self.sheet.write(row, 8, self._get_imgs(product))
            self.sheet.write(row, 9, product_url[n])
            if self.save_img:
                i = SaveImg(row, product.get_images_url(product.get_image_page()))
            print('Progress:', str(row) + '/' + str(len(product_url)), end='\r')
            time.sleep(5)

    def _get_imgs(self, product):
        imgs = ''
        gimgs = product.get_images_url(product.get_image_page())
        count = 0
        for i in gimgs:
            count += 1
            imgs += str(i)
            if count is not len(gimgs):
                imgs += '\n'
        return imgs

    def _get_details(self, product):
        det = ''
        dets = product.get_packaging_details()
        count = 0
        for d in dets:
            count += 1
            for key, value in d.items():
                det += key + ' ' + value
                if count is not len(d):
                    det += '\n'
        return det

    def _get_spec(self, product):
        spec = ''
        specs = product.get_specifics()
        count = 0
        for ss in specs:
            count += 1
            for key, value in ss.items():
                spec += str(key) + ' ' + str(value)
                if count is not len(ss):
                    spec += '\n'
        return spec

    def _get_options(self, product):
        options = product.get_options()
        op = ''
        for option in options:
            for key, values in option.items():
                value = ''
                for val in values:
                    value += str(val) + ', '
            op += str(key) + ' ' + value + '\n'
        return op
