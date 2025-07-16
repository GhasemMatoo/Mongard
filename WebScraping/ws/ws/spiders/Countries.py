import scrapy
from w3lib.html import remove_tags


class CountriesSpider(scrapy.Spider):
    name = "Countries"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]

    def parse(self, response, **kwargs):
        for country in response.css('div.country'):
            name = remove_tags(country.css('h3.country-name').get()).strip()
            capital = country.css('span.country-capital::text').get()
            population = country.css('span.country-population::text').get()

            yield {
                'name': name,
                'capital': capital,
                'population': population
            }
