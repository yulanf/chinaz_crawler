import os
import time
import redis
from baseConfig import *

def create_folder():
    print('create folder.....')
    if not os.path.exists(IPVersion_PATH):
        os.makedirs(SCREEN_SHOT_PATH)
        os.makedirs(SRC_PATH)
        os.makedirs(NETWORK_LOG_PATH)
    else:
        return


create_folder()

def chck_chrome():
    '''检查chrome进程
    检查下有没有异常的chrome进程有就清除
    '''
    cp = os.popen('ps -ef | grep chrome| grep -v grep').readlines()
    if len(cp) != 0:
        os.system('ps -ef | grep chrome | grep -v grep | awk \'{print $2}\' | xargs kill -9')
    else:
        pass


def start_pro():
    os.system('nohup python3 get_page.py f1 >> ' + IPVersion_PATH + 'screenshotv6.log-1 2>&1 &')
    os.system('nohup python3 get_page.py f2 >> ' + IPVersion_PATH + 'screenshotv6.log-2 2>&1 &')


r = redis.Redis(**REDIS_HOST)
while True:
    if r.scard('screenshot') == 0: # redis没东西了就退出
        break
   
    u = os.popen('ps -ef | grep get_page| grep -v grep').readlines()

    if len(u) == 2:
        continue

    if len(u) == 1:
        print('recovering')
        os.system('ps -ef | grep get_page | grep -v grep | awk \'{print $2}\' | xargs kill -9')
        time.sleep(20)
        chck_chrome()
        time.sleep(30)
        start_pro()

    if len(u) == 0:
        print('both break')
        chck_chrome()
        start_pro()
        
        
    time.sleep(5*60)
