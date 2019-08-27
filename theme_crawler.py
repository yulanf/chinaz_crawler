# -*- coding:utf-8 -*-

from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
from storage import RedisClient, MysqlClient, MongoClient
import asyncio
import logging

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
    def __init__(self, ):
        self.redis_db = rc
        self.mysql_db = mc
        self.mongo_db = mc
        self.asession = AsyncHTMLSession()

    async def get_page(self, url):
        '''请求页面

        Args:
            url: 网站url
        Returns:
            r: http响应
        '''
        r = await self.asession.get(url)
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
        soup = BeautifulSoup(html, lxml)
        title = soup.title
        doc = soup.get_text()
        return title

    def get_domain(self):
        '''获取域名'''
        return self.redis_db.pop()

    def get_rest_domain_num(self):
        '''剩余域名数量'''
        return self.redis_db.get_num()

    def save(self):
        with open('title.txt', 'w') as f:
            f.write()

    async def download(self):
        while get_rest_domain_num():
            url = get_domain()
            response = await self.get_page(url)
            doc = self.parse(response)

            save()


    def start(self):
        # 利用asyncio模块进行异步IO处理
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(download())
        loop.run_until_complete(future)

     
        

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
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())