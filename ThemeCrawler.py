from requests_html import HTMLSession
from bs4 import BeautifulSoup
from storage import RedisClient, MysqlClient, MongoClient
from html.parser import HTMLParser
import asyncio
import logging

class ThemeCrawler(object):
    def __init__(self, rc, mc):
        self.redis_db = rc
        self.mysql_db = mc
        # self.mongo_db = mc
        self.session = HTMLSession()

    def get_page(self, url):
        '''请求页面

        Args:
            url: 网站url
        Returns:
            r: http响应
        '''
        r = self.session.get(url, timeout=3)
        return r

    def parse(self, response):
        '''获取所有文字内容:

        从HTTP响应中获取去除了html标签的所有文字内容
        Args:
            response: http响应
        Returns:
            doc: 所有文字内容
        '''
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        title = soup.title.string 
        doc = soup.get_text()
        return title

    def get_domain(self):
        '''获取域名'''
        return self.redis_db.pop()

    def get_rest_domain_num(self):
        '''剩余域名数量'''
        return self.redis_db.get_num()

    def save(self, text):
        '''保存结果'''
        with open('title.txt', 'a+') as f:
            f.write(text)

    def download(self):
        while self.get_rest_domain_num():
            url = self.get_domain()
            logging.info('req ' + url)
            try:
                response = self.get_page(url)
                response.encoding = response.apparent_encoding
                logging.info(response.status_code)
                doc = self.parse(response)
                self.save(url + ';' + doc + '\n')
            except Exception as e:
                self.save(url + ';\n')


if __name__ == '__main__':
    tc = ThemeCrawler(RedisClient('url', '127.0.0.1', None), MysqlClient())
    tc.download()