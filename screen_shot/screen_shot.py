# 截图方式二
# coding=utf-8
from selenium import webdriver
import os
import time
# from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
import multiprocessing
import threading
import redis
from baseConfig import *

r = redis.Redis(**REDIS_HOST)
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none" 

def get_url():
    return r.srandmember('screent_shot_website')

def get_list():
    url_list=[]
    with open('ul.txt', 'r') as f:
        url_list = [line.rstrip() for line in f]
    return url_list


def create_path():
     # 新建文件夹
    if not os.path.exists(SCREEN_SHOT_PATH):
        os.makedirs(SCREEN_SHOT_PATH)
        print("目录新建成功：%s" % SCREEN_SHOT_PATH)
    else:
        print("目录已存在！！！")


def get_screen_shot():

    # 启动参数
    chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--dns-prefetch-disable')

    # chrome_options.add_argument("--kiosk") # full screen for mac
    # driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=desired_capabilities)

    # 初始化driver
    driver = webdriver.Chrome()

    main_win = driver.current_window_handle #记录当前窗口的句柄
    all_win = driver.window_handles

    # driver.maximize_window() # macbook下报错
    # 设置页面最大加载时间
    driver.set_page_load_timeout(5)

    for url in get_list():
        try:
            driver.get('http://' + url) # 此处访问你需要的URL
            driver.save_screenshot(SCREEN_SHOT_PATH + url + '.png')

        except:
            print('exception occurs')
            for win in all_win:
                if main_win != win:
                    print('WIN', win, 'Main', main_win)
                    print('切换到保护罩')
                    driver.close()
                    driver.switch_to.window(win)
                    main_win = win

            js = 'window.open("https://www.baidu.com");'
            driver.execute_script(js)
            # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
            # driver.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
            # driver.execute_script('window.stop()')
            # print('capture in exception')
            continue
        # finally:
        #     print('capture')
        #     driver.save_screenshot(SCREEN_SHOT_PATH + url + '.png')

    driver.quit() 


if __name__ == '__main__':

    # display = Display(visible=0, size=(1920, 1080))
    # display.start()

    create_path()

    # p_lst = []
    # p_num = multiprocessing.cpu_count()
    # for i in range(p_num)
    #     p = multipocessing.Process(target=get_screen_shot,args=('url',))
    #     p_lst.append(p)
    #     p.start()

    # for p in p_lst:
    #     p.join()

    # 多线程
    # threads = []
    # for i in range(2):
    #     t = threading.Thread(target=get_screen_shot)
    #     threads.append(t)

    # # 启动线程
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()
    
    # print('end:%s' % ctime())

    get_screen_shot()

    # display.stop()



   



