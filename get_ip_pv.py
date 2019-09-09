#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from general_crawler import GeneralCrawler
from storage import RedisClient, MysqlClient, WebsiteMetricRepo
import multiprocessing
import requests
import aiohttp
import asyncio
import logging
import demjson
import traceback
import sys
import time

logging.basicConfig(level=logging.INFO,  
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
    datefmt='%a, %d %b %Y %H:%M:%S',  
    # filename='test.log',  
    # filemode='w'
)

class GetIpPv(GeneralCrawler):

    def __init__(self, rc, mc):
        super(GetIpPv, self).__init__(rc, mc)
        self.ip_url = 'https://alexa.chinaz.com/Handlers/GetAlexaIpNumHandler.ashx'
        self.pv_url = 'https://alexa.chinaz.com/Handlers/GetAlexaPvNumHandler.ashx'
 

    async def aget_page(self, url, domain):
        if domain[:4] == 'www.':
            domain = domain[4:]
        else:
            pass
        data = dict(url=domain)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                return await response.text()

    def get_page(self, url, domain):
        '''获取接口数据
        
        Args:
            domain:待查询域名
        Returns:
            r.text:接口返回结果
        '''
        if domain[:4] == 'www.':
            domain = domain[4:]
        else:
            pass
        data = dict(url=domain)
        r = requests.post(url, data=data)
        return r.text

    def parse(self, page_text, field):
        '''获取响应中的特定值

        站长之家返回的接口数据类型为
        [{week: "2019年第22周", StartTime: "2019年07月15日", EndTime: "2019年07月21日", 
        data: {PvNum: "750"}},…]
        此处需要获取最后一个字典的data中的数据
        '''
        # page_text = resp.text()
        p = page_text.find(']')
        page_text = page_text[:p+1]
        resp_list = demjson.decode(page_text)
        if len(resp_list) == 0:
            return 0
        val = int(resp_list[-1]['data'][field])
        return val

    def save(self):
        pass

    def get_result(self, domain):
        # 请求网页获取响应
        ip_resp = self.get_page(self.ip_url, domain)
        pv_resp = self.get_page(self.pv_url, domain)

        # 解析
        ip_num = self.parse(ip_resp, 'IpNum')
        pv_num = self.parse(pv_resp, 'PvNum')
        return (ip_num, pv_num)


    async def aget_result(self, domain):
        '''获取IP_NUM和PV_NUM

        Args:
            domain:域名
        Returns:
            (ip_num, pv_num):(ip值, pv值) 元组
        '''
        # 爬取页面
        logging.info("Send req ip: " + domain)
        ip_resp = await self.aget_page(self.ip_url, domain)
        logging.info("Send req pv: " + domain)
        pv_resp = await self.aget_page(self.pv_url, domain)

        # 解析
        ip_num = self.parse(ip_resp, 'IpNum')
        logging.info('Get res ip: ' + domain + ' ' + ip_num)
        pv_num = self.parse(pv_resp, 'PvNum')
        logging.info('Get res pv: ' + domain + ' ' + pv_num)

        return (ip_num, pv_num)

    async def download(self):
        '''获取结果并保存到Mongo数据库
        '''
        while self.get_num():
            domain = self.get_domain()
         
            result = await self.aget_result(domain)

            # IO操作
            #save()
            print(result)
     

def start():
    '''非协程启动爬虫'''
    rds = RedisClient('url', '127.0.0.1', None)
    my = MysqlClient()
    ip_pv = GetIpPv(rds, my)
    while ip_pv.get_num():

        domain = ip_pv.get_domain()
        print(ip_pv.get_result(domain))

# async def run():
#     rds = RedisClient('url', '127.0.0.1', None)
#     my = MysqlClient()
#     ip_pv = GetIpPv(rds, my)
#     while ip_pv.get_num():

#         domain = ip_pv.get_domain()
#         result = await ip_pv.aget_result(domain)
#         print(result)

def start_coro():
    '''非协程启动爬虫'''
    rds = RedisClient('url', '127.0.0.1', None)
    my = MysqlClient()
    ip_pv = GetIpPv(rds, my)
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(ip_pv.download())
    finally:
        event_loop.close()

if __name__ == '__main__':

    start_coro()
    '''
    # 多进程
    process_list = []
    for i in range(10):#通过循环创建多个子进程
        p = Process(target=start_coro,args=('info%s'%i,0))#创建子进程
        process_list.append(p)#将创建的子进程对象添加到列表中
        p.start()#启动子进程
     
    for p in process_list:
        p.join()   # 之前的所有进程必须在这里都执行完才能执行下面的代码
    '''


    
