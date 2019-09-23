from selenium import webdriver
import os
import time
# from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import threading
from baseConfig import *

class ScreenShotSpider(object):
    """docstring for ScreenShotSpider"""
    def __init__(self):
        self.chrome_options = Options()
        self.browser = webdriver.Chrome()
        # self.browser.set_page_load_timeout(5)

    def browser_quit(self):
        '''退出浏览器'''
        # self.browser.service.process.send_signal(signal.SIGTERM)
        self.browser.quit()
        print('close browser')

    def restart(self):
        self.browser_quit()
        self.browser = webdriver.Chrome()

    def open_new_tag(self):
        self.browser.execute_script('window.open("https://www.baidu.com")')

    def get_screen_shot(self, url):
        '''保存截图'''
        try:
            self.browser.get('http://' + url)
        except TimeoutException:
            print(url + ' ' + '无法访问')
            self.restart()
        else: # 未发生异常
            filename = SCREEN_SHOT_PATH + url + '.png'
            self.browser.save_screenshot(filename)
            print('save ' + filename)

    def get_list(self):
        url_list=[]
        with open('ul.txt', 'r') as f:
            url_list = [line.rstrip() for line in f]
        return url_list


    def run(self):
        for url in self.get_list():
            self.get_screen_shot(url)
        self.browser_quit()

if __name__ == '__main__':
    sss = ScreenShotSpider()
    sss.run()

        