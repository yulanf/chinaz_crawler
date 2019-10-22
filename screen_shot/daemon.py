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


r = redis.Redis(**REDIS_HOST)
while True:
    if r.scard('screenshot') == 0: # redis没东西了就退出
        break
   
    u = os.popen('ps -ef | grep get_page| grep -v grep').readlines()

    if len(u) == 2:
        continue

    if len(u) == 1:
        if 'f1' in u[0]:
            os.system('nohup python3 get_page.py f2 >> ' + IPVersion_PATH + 'screenshotv6.log-2 2>&1 &')
        if 'f2' in u[0]: 
            os.system('nohup python3 get_page.py f1 >> ' + IPVersion_PATH + 'screenshotv6.log-1 2>&1 &')

    if len(u) == 0:
        print('both break')
        os.system('nohup python3 get_page.py f1 >> ' + IPVersion_PATH + 'screenshotv6.log-1 2>&1 &')
        os.system('nohup python3 get_page.py f2 >> ' + IPVersion_PATH + 'screenshotv6.log-2 2>&1 &')

        
    time.sleep(600)
