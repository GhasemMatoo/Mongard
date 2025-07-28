# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose


def to_strip(value):
    return value.strip()


def to_uppercase(value):
    return value.upper()


class WsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CountryItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags, to_strip, to_uppercase), output_processor=TakeFirst())
    capital = scrapy.Field(output_processor=TakeFirst())
    population = scrapy.Field(output_processor=TakeFirst())


class FileItem(scrapy.Item):
    file_url = scrapy.Field()
    files = scrapy.Field()
