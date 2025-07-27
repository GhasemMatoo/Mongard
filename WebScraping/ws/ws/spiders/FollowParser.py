import scrapy
from w3lib.html import remove_tags


class FollowParserSpider(scrapy.Spider):
    name = "followparsers"
    allowed_domains = ["www.bike-discount.de"]
    start_urls = [
        'https://www.bike-discount.de/en/bike',
    ]

    def parse(self, response, **kwargs):
        for bike in response.css('div.product--info'):
            link = bike.css('a.product--title::attr(href)').get()
            yield scrapy.Request(link, callback=self.parse_bike)

    def parse_bike(self, response, **kwargs):
        price = response.css('#netz-price::text').get()
        yield {'price': price}
