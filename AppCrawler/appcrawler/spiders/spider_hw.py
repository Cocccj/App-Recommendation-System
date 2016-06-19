import scrapy
import re
from scrapy.selector import Selector
from appcrawler.items import AppcrawlerItem

class HuaweiSpider(scrapy.Spider):
    name = "hwspider"
    allowed_domains = ["huawei.com"]

    start_urls = [
        "http://appstore.huawei.com/more/all/1",
        "http://appstore.huawei.com/more/recommend/1",
        "http://appstore.huawei.com/more/soft/1",
        "http://appstore.huawei.com/more/game/1",
        "http://appstore.huawei.com/more/newPo/1",
        "http://appstore.huawei.com/more/newUp/1",
    ]

    def find_next_page(self, url):
        try:
            num_page = url.split('/')[-1]
            url = url[:-len(num_page)] + str(int(num_page) + 1)
            return url
        except ValueError as ve:
            print ve.message

    def parse(self, response):
        page = Selector(response)
        hrefs = page.xpath('//h4[@class="title"]/a/@href')

        for href in hrefs:
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })

    def parse_item(self, response):
        page = Selector(response)
        item = AppcrawlerItem()
        item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
        item['url'] = response.url
        item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)
        item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')
        #item['thumbnailurl'] = page.xpath('//url[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@lazyload').extract_first()

        divs = page.xpath('//div[@class="open-info"]')
        recom = ""
        for d in divs:
            url = d.xpath('./p[@class="name"]/a/@href').extract_first()
            recommended_app = re.match(r'http://.*/(.*)', url).group(1)
            name = d.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
            recom += "{0}:{1},".format(recommended_app, name)
        item['recommended'] = recom
        yield item
