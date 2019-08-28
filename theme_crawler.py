# -*- coding:utf-8 -*-

from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
from storage import RedisClient, MysqlClient, MongoClient
from html.parser import HTMLParser
import asyncio
import logging

logging.basicConfig(level=logging.WARNING,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    # filename='test.log',  
                    # filemode='w'
                    )

class PureTextExtractor(HTMLParser):
    # def handle_starttag(self, tag, attrs):
    #     print("Encountered a start tag:", tag)

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("", data)

    def main(self):
        parser = PureTextExtractor()
        parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html><script>script here</script>')


class ThemeCrawler(object):
    def __init__(self, rc, mc):
        self.redis_db = rc
        self.mysql_db = mc
        # self.mongo_db = mc
        self.asession = AsyncHTMLSession()

    async def get_page(self, url):
        '''请求页面

        Args:
            url: 网站url
        Returns:
            r: http响应
        '''
        r = await self.asession.get(url, timeout=3)
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

    async def save(self, text):
        '''保存结果'''
        with open('title.txt', 'a+') as f:
            f.write(text)

    async def download(self):
        while self.get_rest_domain_num():
            url = self.get_domain()
            logging.info('req ' + url)
            try:
                response = await self.get_page(url)
                response.encoding = response.apparent_encoding
                logging.info(response.status_code)
                doc = self.parse(response).strip()
                await self.save(url + ';' + doc + '\n')
            except Exception as e:
                await self.save(url + ';\n')

    def start(self):
        # 利用asyncio模块进行异步IO处理
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(download())
        loop.run_until_complete(start())

     
class Spider_aio(object):
    def __init__(self):
        pass

    async def get_page(self, client, url):
        async with client.get(url) as resp:
            assert resp.status == 200
            return await resp.text()

    async def parse(self, content):
        parser = PureTextExtractor()
        parser.feed(content)

    async def main(self):
        async with aiohttp.ClientSession() as client:
            html = await getpage(client)



if __name__ == '__main__':
    tc = ThemeCrawler(RedisClient('url', '127.0.0.1', None), MysqlClient())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tc.download())
