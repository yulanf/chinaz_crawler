#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from general_crawler import *
import logging

class GetIpPv(GeneralCrawler):
    def __init__():
        self.ip_url = 'https://alexa.chinaz.com/Handlers/GetAlexaIpNumHandler.ashx'
        self.pv_url = 'https://alexa.chinaz.com/Handlers/GetAlexaPvNumHandler.ashx'
 
    def get_page(self, url, ):
        if url[:4] == 'www.':
            url = url[4:]
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

    def crawl():
        # 获取域名
        url = self.get_domain()
        # 请求网页获取响应
        ip_res = get_page(self.ip_url)
        pv_res = get_page(self.pv_url)

        # 解析
        parse(ip_res, 'IpNum')
        parse(pv_res, 'PvNum')
        # 保存
        save()

def crawl():
    while get_domain():
        get_page('')
        parse
        save
if __name__ == '__main__':
    crawl_ip_pv = GetIpPv(key, host, password)
    crawl_ip_pv.get_num()
