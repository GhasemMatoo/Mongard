import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/Bruce_Lee",
        "https://en.wikipedia.org/wiki/Carl_Sagan",
        "https://en.wikipedia.org/wiki/Marie_Curie"
    ]

    def parse(self, response, **kwargs):
        # title = response.css('title').extract()
        title_css = response.css('title::text').get()
        # title = response.xpath('/html/head/title').get()
        title = response.xpath('/html/head/title/text()').get()
        role = response.css('div#p-vector-user-menu-overflow::attr(class)').get()
        yield {
            'title_css': title_css,
            'title_xpath': title,
            'attr': role
        }
