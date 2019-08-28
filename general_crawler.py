#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import aiohttp
import demjson
import traceback
import sys
import time
from multiprocessing import Process, Queue


class GeneralCrawler(object):
    def __init__(self, rc, mc):
        self.redis_db = rc
        self.mysql_db = mc

    def get_page(self, url, data):
        '''获取页面
        
        爬取url对应的页面
        Args:
            url
            data
        Returns:
            r.text:页面文本
        '''
        pass

    def parse(self, page_text):
        '''解析页面'''
        pass


    def get_domain(self):
        '''获取域名'''
        return self.redis_db.pop()

    def get_num(self):
        return self.redis_db.get_num()

    def save(self):
        '''存储'''
        pass

    def crawl(self):
        pass
        
