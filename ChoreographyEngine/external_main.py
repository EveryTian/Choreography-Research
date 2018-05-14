#! python3
# coding: utf-8

from threading import Thread
import main

if __name__ == '__main__' and main.check_setting():
    Thread(target=main.listen).start()
