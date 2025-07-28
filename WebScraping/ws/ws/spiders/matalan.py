import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MatalanSpider(CrawlSpider):
    name = "matalan"
    allowed_domains = ["www.matalan.co.uk/"]
    start_urls = ["https://www.matalan.co.uk/mens/suits.list", ]

    rules = (Rule(LinkExtractor(allow=r'clothing/'), callback="parse_item", follow=False),)

    def parse_item(self, response):
        item = {}
        item['product_id'] = response.css('#productDetails > div > section > div > div:nth-child(4) > div::text').get()
        print(response)
        return item
