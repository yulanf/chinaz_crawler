import aiohttp
from html.parser import HTMLParser

class PureTextExtractor(HTMLParser):
    # def handle_starttag(self, tag, attrs):
    #     print("Encountered a start tag:", tag)

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("", data)


class Spider(object):
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



# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())