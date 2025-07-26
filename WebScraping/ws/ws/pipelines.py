# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from scrapy.exceptions import DropItem


class WsPipeline:
    def process_item(self, item, spider):
        return item


class CountryPipeline:
    def __init__(self):
        self.con = sqlite3.connect('countries.db')
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS countries(name TEXT PRIMARY KEY, capital TEXT, population INTEGER)
        """)

    def process_item(self, item, spider):
        self.create_table()
        self.cur.execute("""
        INSERT OR IGNORE INTO countries VALUES (?, ?, ?)""",
                         (item['name'], item['capital'], int(item['population'])))
        self.con.commit()
        return item


class PopulationPipeline:
    def process_item(self, item, spider):
        if int(item['population']) <= 50000000:
            print("==" * 90)
            raise DropItem('population is less than 50M...')
        else:
            return item
