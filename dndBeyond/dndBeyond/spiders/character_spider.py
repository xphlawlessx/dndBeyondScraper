import scrapy
from scrapy.loader import ItemLoader
from dndBeyond.items import DndbeyondItem
import os


class CharacterSpider(scrapy.Spider):
    name = "character"
    cwd = os.getcwd().replace('\\', '/')
    start_urls = [f'file://{cwd}/test.html']

    def parse(self, response):
        loader = ItemLoader(item=DndbeyondItem(), response=response)
        loader.add_xpath('name',
                         "//div[@class='ct-character-tidbits__name']//text()")
        loader.add_xpath('stats',
                         "//div[@class='ct-quick-info__abilities']//text()")
        loader.add_xpath('skills',
                         "//div[@class='ct-skills__item']//text()")
        yield loader.load_item()