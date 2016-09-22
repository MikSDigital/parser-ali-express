#!/usr/bin/env python3
from export import AliExport
import socket
import socks


if __name__ == '__main__':
    save_imgs = False
    url_ali = input('Enter Market URL: ')
    ask_tor = input('Use TOR connection? (y/n): ')
    ask_save_image = input('Save images? (y/n): ')

    if ask_tor.lower() == 'y':
        socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
        socket.socket = socks.socksocket

    if ask_save_image.lower() == 'y':
        save_imgs = True

    ex = AliExport(url_ali, save_imgs)
