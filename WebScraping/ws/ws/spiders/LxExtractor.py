import scrapy
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags


class LxExtractorSpider(scrapy.Spider):
    name = "lxextractor"
    allowed_domains = ["www.bike-discount.de"]
    start_urls = [
        'https://www.bike-discount.de/en/bike'
    ]
    le_extractor = LinkExtractor(allow='contact')

    def parse(self, response, **kwargs):
        links = self.le_extractor.extract_links(response=response)
        for link in links:
            yield {'link': link}
