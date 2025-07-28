import scrapy
from scrapy.crawler import CrawlerProcess


class RoocketSpider(scrapy.Spider):
    name = 'roocket'

    def start_requests(self):
        yield scrapy.Request('https://roocket.ir/series/')

    def parse(self, response, **kwargs):
        for fara in response.css("a>img"):
            title = fara.attrib["alt"]
            yield {'title': title}


process = CrawlerProcess(
    settings={
        'FEEDS': {
            'roocket.json': {'format': 'json', 'encoding': 'utf8'},
            'roocket.csv': {'format': 'csv', 'encoding': 'utf8'},
        }
    }
)

process.crawl(RoocketSpider)
process.start()
