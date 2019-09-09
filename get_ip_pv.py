#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from general_crawler import GeneralCrawler
from storage import RedisClient, MysqlClient, MongoClient
from multiprocessing import Pool
import requests
import aiohttp
import asyncio
import logging
import demjson
import traceback
import sys
import time

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
        '''获取结果

        Args:
            domain:域名
        Returns:
            (ip_num, pv_num):(ip值，pv值) 元组
        '''
        # 爬取页面
        ip_resp = await self.aget_page(self.ip_url, domain)
        pv_resp = await self.aget_page(self.pv_url, domain)

        # 解析
        ip_num = self.parse(ip_resp, 'IpNum')
        pv_num = self.parse(pv_resp, 'PvNum')

        return (ip_num, pv_num)

def start():
    '''非协程启动爬虫'''
    rds = RedisClient('url', '127.0.0.1', None)
    my = MysqlClient()
    ip_pv = GetIpPv(rds, my)
    while ip_pv.get_num():

        domain = ip_pv.get_domain()
        print(ip_pv.get_result(domain))

async def run():
    rds = RedisClient('url', '127.0.0.1', None)
    my = MysqlClient()
    ip_pv = GetIpPv(rds, my)
    while ip_pv.get_num():

        domain = ip_pv.get_domain()
        result = await ip_pv.aget_result(domain)
        print(result)


if __name__ == '__main__':
    # start()
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(run())
    finally:
        event_loop.close()


    # 多进程
    pool = Pool(processes=10)
    for i in range():
        res = pool.apply_async(os.getpid, ())


    
