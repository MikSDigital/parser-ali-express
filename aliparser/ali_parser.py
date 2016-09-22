from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import time


class AliParser():
    def __init__(self, start_page):
        self.pages = []
        self._get_links_to_products(start_page)

    def _get_links_to_products(self, link_to_page):
        try:
            html = urlopen(link_to_page)
        except HTTPError as e:
            print(e)
            return None
        try:
            bs_obj = BeautifulSoup(html, 'html.parser')

            p = bs_obj.findAll('h3')
            for link in p:
                for a in link.findAll('a', href=re.compile('(^http\:\/\/www\.aliexpress\.com\/store\/product\/)[A-Za-z0-9\-]+\/[0-9]+\_[0-9]+(\.html)$')):
                    new_page = a.attrs['href']
                    self.pages.append(new_page)
            next_page = self._get_next_page(link_to_page)
            if next_page is not None:
                time.sleep(10)
                self._get_links_to_products(next_page)
        except AttributeError as e:
            print(e)
            return None

    def _get_next_page(self, current_page):
        html = urlopen(current_page)
        bs_obj = BeautifulSoup(html, 'html.parser')
        ltnp = (bs_obj.find(
            'a',
            {'class':'ui-pagination-next'}
        ))
        if ltnp is not None:
            self.link_to_next_page = 'https:' + ltnp.attrs['href']
            return self.link_to_next_page
        else:
            return None

    # Functions for test
    def return_pages(self):
        return self.pages

    def retutn_link_to_next_page(self):
        return self.link_to_next_page
