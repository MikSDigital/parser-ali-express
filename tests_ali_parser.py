#!/usr/bin/env python3
import unittest
from aliparser.ali_parser import AliParser


class TestAliParser(unittest.TestCase):
    def setUp(self):
        self.main_url = 'http://makibes.aliexpress.com/store/all-wholesale-products/1086467.html'
        self.parser = AliParser(self.main_url)
        self.url_to_first_product = 'http://www.aliexpress.com/store/product/Xiaomi-Mi-Band-1S-pulse-miband-heart-rate-Monitor-IP67-Smart-Bluetooth-4-0-Wristband-Bracelet/1086467_32537756174.html'
        self.url_to_last_product_on_shop = 'http://www.aliexpress.com/store/product/UC30-1080P-Portable-Mini-Led-Projector-HDMI-Home-Theater-MINI-Projector-Support-HDMI-VGA-AV-USB/1086467_2041694092.html'
        self.p = self.parser.return_pages()

    def test_get_link_to_next_page(self):
        """
        Link to next page must be equal to next_link
        """
        next_link = 'https://makibes.aliexpress.com/store/1086467/search/6.html?origin=n'
        get_next_link = self.parser.retutn_link_to_next_page()
        self.assertEqual(get_next_link, next_link)

    def test_first_n_last_product_in_shop(self):
        """
        Links to first and last products in shop must be equal
        f_pr and l_pr
        """
        self.assertEqual(self.p[0], self.url_to_first_product)
        self.assertEqual(self.p[186], self.url_to_last_product_on_shop)

if __name__ == '__main__':
    unittest.main()
