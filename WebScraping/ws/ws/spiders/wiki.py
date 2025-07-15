import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/Bruce_Lee",
        "https://en.wikipedia.org/wiki/Carl_Sagan",
    ]

    def parse(self, response, **kwargs):
        title = response.css('title').extract()
        yield {'title': title}

