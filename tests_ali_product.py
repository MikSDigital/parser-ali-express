#!/usr/bin/env python3
import unittest
from aliparser.ali_product import AliProduct


class AliProductTest(unittest.TestCase):
    def setUp(self):
        self.url_product = AliProduct('https://www.aliexpress.com/item/3-colors-2015-hot-selling-women-s-leggings-blue-and-black-jean-girls-Leggings-with-2/32460006955.html?spm=2114.30010308.3.47.ihCU4t&s=p&ws_ab_test=searchweb201556_7,searchweb201602_5_10057_10056_10065_10037_10068_10055_10054_10069_301_10059_10058_10032_10073_10017_10070_9931_10060_10061_10052_10062_10053_10050_10051,searchweb201603_2&btsid=ad6c3b4a-9a6e-482b-aba4-6a369b4b3de9')
        self.url_product_two = AliProduct('https://www.aliexpress.com/store/product/Makibes-JW018-BT4-0-Smart-band-bracelet-Heart-Rate-Monitor-Activity-fitness-Tracker-Wristband-for-IOS/1086467_32548514285.html')

    def test_get_product_name(self):
        """
        Product name must be equal to title
        """
        title = "3 colors 2015 hot selling women's leggings blue and black jean girls Leggings with 2 real pockets FREE SHIPPING"
        get_title = self.url_product.get_title()
        self.assertEqual(get_title, title)

    def test_get_price(self):
        """
        In AliExpress have 3 types of prices:
            'del' price
            low-high price
            just price

        Just price = $25.49
        low-high price = $19.69 - 23.99
        del price = $8.88
        """
        price = '$25.49'
        lh_price = '$19.69 - 23.99'
        d_price = '$8.88'

        link_lh_price = AliProduct("https://www.aliexpress.com/store/product/Makibes-ID107-Bluetooth-4-0-Smart-Bracelet-smart-band-Heart-Rate-Monitor-Wristband-Fitness-Tracker-for/1086467_32615898626.html")

        get_d_price = self.url_product.get_price()
        get_lh_price = link_lh_price.get_price()
        get_price = self.url_product_two.get_price()

        self.assertEqual(get_d_price, d_price)
        self.assertEqual(get_lh_price, lh_price)
        self.assertEqual(get_price, price)

    def test_get_discount_price(self):
        """
        Discount price should be equal $7.55 or ' '
        """
        f_price = '$7.55'
        s_price = ' '

        get_f_price = self.url_product.get_discount_price()
        get_s_price = self.url_product_two.get_discount_price()

        self.assertEqual(get_f_price, f_price)
        self.assertEqual(get_s_price, s_price)

    def test_get_options(self):
        """
        Create list
        colors: Black, BLue, Dark Grey
        sizes: S, M, L, XL, XXL
        options = [{'Colors: ': colors}, {'Size: ': sizes}]
        """
        colors = ['Black ', 'Blue ', 'Dark Grey ']
        sizes = ['S ', 'M ', 'L ', 'XL ', 'XXL ']
        options = [
            {'Color: ': colors},
            {'Size: ': sizes}
        ]

        get_options = self.url_product.get_options()
        self.assertEqual(get_options, options)

    @unittest.expectedFailure
    def test_get_item_specifics(self):
        """
        Get item specifics
        spec = [
            {'Brand name: ': 'Makibes'},
            {'Application Age Group: ': 'Adult '},
            ...
        ]
        """
        spec = [
            {'Item Type: ': 'Leggings '},
            {'Pattern Type: ': 'Solid '},
            {'Fabric Type: ': 'Knitted '},
            {'Length: ': 'Ankle-Length '},
            {'Model Number: ': '001 '},
            {'Gender: ': 'Women'},
            {'Waist Type': 'Mid'},
            {'Material: ': 'Polyester,Spandex'},
            {'Thickness: ': 'Standard '}
        ]
        get_spec = self.url_product.get_specifics()
        self.assertEqual(get_spec, spec)

    def test_get_packaging_details(self):
        """
        pack = [
            {'Unit type: ': 'piece '},
            ....
        ]
        """
        pack = [
            {'Unit Type: ': 'piece '},
            {'Package Weight: ': '0.130kg (0.29lb.) '},
            {'Package Size: ': '20cm x 10cm x 10cm (7.87in x 3.94in x 3.94in) '}
        ]
        get_pack = self.url_product.get_packaging_details()
        self.assertEqual(get_pack, pack)

    def test_get_img_page(self):
        """
        get link to page with images
        """
        image_page = 'https://www.aliexpress.com/item-img/3-colors-2015-hot-selling-women-s-leggings-blue-and-black-jean-girls-Leggings-with-2/32460006955.html'
        get_img_page = self.url_product.get_image_page()
        self.assertEqual(get_img_page, image_page)

    def test_get_images(self):
        """
        Get links to images from img page
        """
        get_imgs = self.url_product.get_images_url('https://www.aliexpress.com/item-img/3-colors-2015-hot-selling-women-s-leggings-blue-and-black-jean-girls-Leggings-with-2/32460006955.html')
        imgs = [
            'https://ae01.alicdn.com/kf/HTB1PVXMLFXXXXasXFXXq6xXFXXXZ/3-colors-2015-hot-selling-women-s-leggings-blue-and-black-jean-girls-Leggings-with-2.jpg',
            'https://ae01.alicdn.com/kf/HTB1bzNWLFXXXXaAXpXXq6xXFXXXp/3-colors-2015-hot-selling-women-s-leggings-blue-and-black-jean-girls-Leggings-with-2.jpg',
            'https://ae01.alicdn.com/kf/HTB1XrJVLFXXXXbtXpXXq6xXFXXX5/3-colors-2015-hot-selling-women-s-leggings-blue-and-black-jean-girls-Leggings-with-2.jpg',
            'https://ae01.alicdn.com/kf/HTB1dRBRLFXXXXcLXpXXq6xXFXXXO/3-colors-2015-hot-selling-women-s-leggings-blue-and-black-jean-girls-Leggings-with-2.jpg',
            'https://ae01.alicdn.com/kf/HTB1kWJ8LFXXXXXOXXXXq6xXFXXXb/3-colors-2015-hot-selling-women-s-leggings-blue-and-black-jean-girls-Leggings-with-2.jpg'
        ]
        self.assertEqual(get_imgs, imgs)

if __name__ == "__main__":
    unittest.main()
