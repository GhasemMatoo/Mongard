import scrapy
from ..items import FileItem


class FiledownloadSpider(scrapy.Spider):
    name = "FileDownload"
    allowed_domains = ["faradars.org"]
    start_urls = ["https://roocket.ir/series/"]

    def parse(self, response, **kwargs):
        items = FileItem()
        image_urls = []
        for fara in response.css("a>img"):
            image_url = fara.css('img').attrib['src']
            image_urls.append(image_url)
        items['file_url'] = image_urls
        yield items