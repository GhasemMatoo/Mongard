import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from ..items import CountryItem


class CountriesItemsSpider(scrapy.Spider):
    name = "CountriesItems"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]

    def parse(self, response, **kwargs):
        items = CountryItem()
        for country in response.css('div.country'):
            items['name'] = remove_tags(country.css('h3.country-name').get()).strip()
            items['capital'] = country.css('span.country-capital::text').get()
            items['population'] = country.css('span.country-population::text').get()

        yield items
