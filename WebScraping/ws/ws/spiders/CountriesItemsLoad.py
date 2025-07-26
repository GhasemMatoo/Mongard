import scrapy
from scrapy.loader import ItemLoader
from ..items import CountryItem


class CountriesItemsLoadSpider(scrapy.Spider):
    name = "CountriesItemsLoad"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]

    def parse(self, response, **kwargs):
        for country in response.css('div.country'):
            l_items = ItemLoader(item=CountryItem(), selector=country)
            l_items.add_css('name', 'h3.country-name')
            l_items.add_css('capital', 'span.country-capital::text')
            l_items.add_css('population', 'span.country-population::text')
            yield l_items.load_item()
