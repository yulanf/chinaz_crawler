# -*- coding:utf-8 -*-
from selenium import webdriver
import os
import time
import json
# from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import threading
import queue
from baseConfig import *
import logging
import redis
from multiprocessing import Process

from selenium import webdriver
from PIL import Image
from io import BytesIO

logging.basicConfig(level=logging.INFO,  
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
    datefmt='%a, %d %b %Y %H:%M:%S',  
    # filename='screenshot.log',  
    # filemode='a+'
)

class ScreenShotSpider(threading.Thread):
    """docstring for ScreenShotSpider"""
    def __init__(self, q=None):
        super(ScreenShotSpider, self).__init__()
        self.dc = DesiredCapabilities.CHROME
        self.dc['loggingPrefs'] = {'performance': 'ALL'}

        self.chrome_options = Options()
        self.chrome_options.add_experimental_option('w3c', False) # figure out invalid argument: log type 'performance' not found

        self.chrome_options.add_argument('--no-sandbox') # root下启动
        self.chrome_options.add_argument('--window-size=1920,1080') #指定浏览器分辨率
        self.chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        # self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--headless') # 无界面启动

        self.browser = webdriver.Chrome(options=self.chrome_options, desired_capabilities=self.dc)
        # self.browser.set_page_load_timeout(5) # 等待加载时间
        self.q = q
        self.r = redis.Redis(**REDIS_HOST)

    def browser_quit(self):
        '''退出浏览器'''
        # self.browser.service.process.send_signal(signal.SIGTERM)
        self.browser.quit()
        logging.debug('close browser')

    def restart(self):
        '''重启浏览器'''
        logging.warning('restarting')
        self.browser_quit()
        self.browser = webdriver.Chrome(options=self.chrome_options, desired_capabilities=self.dc)

    def open_new_tag(self):
        '''开启新标签页'''
        self.browser.execute_script('window.open("https://www.baidu.com")')

    def full_screenshot(self, driver, save_path):
        '''全屏截图'''
        # initiate value
        save_path = save_path + '.png' if save_path[-4::] != '.png' else save_path
        img_li = []  # to store image fragment
        offset = 0  # where to start

        # js to get height
        height = driver.execute_script('return Math.max('
                                       'document.documentElement.clientHeight, window.innerHeight);')

        # js to get the maximum scroll height
        # Ref--> https://stackoverflow.com/questions/17688595/finding-the-maximum-scroll-position-of-a-page
        max_window_height = driver.execute_script('return Math.max('
                                                  'document.body.scrollHeight, '
                                                  'document.body.offsetHeight, '
                                                  'document.documentElement.clientHeight, '
                                                  'document.documentElement.scrollHeight, '
                                                  'document.documentElement.offsetHeight);')

        # looping from top to bottom, append to img list
        # Ref--> https://gist.github.com/fabtho/13e4a2e7cfbfde671b8fa81bbe9359fb
        while offset < max_window_height:

            # Scroll to height
            driver.execute_script(f'window.scrollTo(0, {offset});')
            img = Image.open(BytesIO((driver.get_screenshot_as_png())))
            img_li.append(img)
            offset += height

        # Stitch image into one
        # Set up the full screen frame
        img_frame_height = sum([img_frag.size[1] for img_frag in img_li])
        img_frame = Image.new('RGB', (img_li[0].size[0], img_frame_height))
        offset = 0
        for img_frag in img_li:
            img_frame.paste(img_frag, (0, offset))
            offset += img_frag.size[1]
        img_frame.save(save_path)

    def get_website_info(self, url):
        '''保存相关内容

        保存首页截图、首页源代码、流量日志
        '''
        try:
            self.browser.get('http://' + url)
        except:
            logging.warning(url + ' ' + '无法访问')
            self.restart()
        else: # 未发生异常
            # 保存截图
            pic_name = SCREEN_SHOT_PATH + url + '.png'
            # self.browser.save_screenshot(pic_name)   
            self.full_screenshot(self.browser, pic_name)
            logging.debug('save ' + pic_name)

            # 保存源代码
            page_src_name = SRC_PATH + url + '.html'
            with open(page_src_name, 'w') as f1:
                f1.write(self.browser.page_source)
            logging.debug('save ' + page_src_name)

            # 保存访问日志
            network_log_name = NETWORK_LOG_PATH + url + '.json'
            browser_logs = [json.loads(browser_log['message'])['message'] for browser_log in self.browser.get_log('performance')]
            with open(network_log_name , 'w') as f2:
                json.dump(browser_logs, f2)
            logging.debug('save ' + network_log_name)

            logging.info('save ' + url)

    def get_list(self):
        '''从文件读取url列表'''
        url_list=[]
        with open('ul.txt', 'r') as f:
            url_list = [line.rstrip() for line in f]
        return url_list


    # def run(self):
        '''从文件读取url列表'''
    #     while True:
    #         # 队列空为True，则break掉
    #         if self.q.empty():
    #             break
    #         url = self.q.get()
    #         logging.debug(threading.currentThread().getName() + ' ' + url)
    #         self.get_website_info(url)

    #     self.browser_quit()

    #     for url in self.get_list():
    #         self.get_website_info(url)
    #     self.browser_quit()

    def run(self):
        '''从redis读取url'''
        while self.r.scard(SCREEN_SHOT_KEY):
            # url = self.r.srandmember(SCREEN_SHOT_KEY)
            url = self.r.spop(SCREEN_SHOT_KEY)
            logging.debug(threading.currentThread().getName() + ' ' + url)
            self.get_website_info(url)
        
        self.browser_quit()


def url_queue():
    '''把url加到队列里'''
    q = queue.Queue()
    with open('aaaa_1.txt', 'r') as f:
        for line in f:
            q.put(line.rstrip())
    return q

def run_threading(thread_num):
    # q = url_queue()
    spider_lst = []
    for i in range(thread_num):
        t = ScreenShotSpider()
        t.start()
        spider_lst.append(t)

    for t in spider_lst:
        t.join()

if __name__ == '__main__':
    logging.info('screenshot program starting...')
    # display = Display(visible=0, size=(1920, 1080))
    # display.start()

    # p_lst = []
    # for i in range(2):
    #     p = Process(target=run_threading, args=(2,))
    #     p.start()
    #     p_lst.append(p)
    
    # for p in p_lst:
    #     p.join()

    run_threading(2)
    # display.stop()

