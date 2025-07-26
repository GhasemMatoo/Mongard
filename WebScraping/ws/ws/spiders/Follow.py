import scrapy
from w3lib.html import remove_tags


class FollowSpider(scrapy.Spider):
    name = "follow"
    allowed_domains = ["www.bike-discount.de"]
    start_urls = [
        'https://www.bike-discount.de/en/bike'
    ]

    def parse(self, response, **kwargs):
        for bike in response.css('div.product--box'):
            name = remove_tags(bike.css('a.product--title').get()).strip()
            price = remove_tags(bike.css('.product--price').get()).strip()
            yield {'name': name, 'price': price}

        next_page = response.css('a[title="Next page"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)