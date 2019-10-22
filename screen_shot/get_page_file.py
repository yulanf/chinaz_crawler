# -*- coding:utf-8 -*-
from selenium import webdriver
import os
import time
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import threading
import queue
from baseConfig import *
import logging

logging.basicConfig(level=logging.INFO,  
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
    datefmt='%a, %d %b %Y %H:%M:%S',  
    # filename='test.log',  
    # filemode='w'
)

class ScreenShotSpider(threading.Thread):
    """docstring for ScreenShotSpider"""
    def __init__(self, q):
        super(ScreenShotSpider, self).__init__()
        self.chrome_options = Options()

        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--window-size=1920,1080') #指定浏览器分辨率
        self.chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        # self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--headless')

        self.browser = webdriver.Chrome(options=self.chrome_options)
        self.browser.set_page_load_timeout(5)
        self.q = q

    def browser_quit(self):
        '''退出浏览器'''
        # self.browser.service.process.send_signal(signal.SIGTERM)
        self.browser.quit()
        logging.info('close browser')

    def restart(self):
        logging.warning('restarting')
        self.browser_quit()
        self.browser = webdriver.Chrome(options=self.chrome_options)

    def open_new_tag(self):
        self.browser.execute_script('window.open("https://www.baidu.com")')

    def get_screen_shot(self, url):
        '''保存截图'''
        try:
            self.browser.get('http://' + url)
        except TimeoutException:
            logging.info(url + ' ' + '无法访问')
            self.restart()
        else: # 未发生异常
            filename = SCREEN_SHOT_PATH + url + '.png'
            self.browser.save_screenshot(filename)
            logging.info('save ' + filename)

    def get_list(self):
        url_list=[]
        with open('ul.txt', 'r') as f:
            url_list = [line.rstrip() for line in f]
        return url_list


    def run(self):
        while True:
            # 队列空为True，则break掉
            if self.q.empty():
                break
            url = self.q.get()
            logging.info(threading.currentThread().getName() + ' ' + url)
            self.get_screen_shot(url)

        self.browser_quit()

        # for url in self.get_list():
        #     self.get_screen_shot(url)
        # self.browser_quit()


def url_queue():
    q = queue.Queue()
    with open('aaaa_1.txt', 'r') as f:
        for line in f:
            q.put(line.rstrip())
    return q

if __name__ == '__main__':
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    q = url_queue()
    spider_lst = []
    for i in range(2):
        t = ScreenShotSpider(q)
        t.start()
        spider_lst.append(t)

    for t in spider_lst:
        t.join()

    display.stop()

        
