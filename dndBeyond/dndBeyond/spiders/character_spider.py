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
        stats = response.xpath("//div[@class=' ct-ability-summary']")
        loader.add_value('stats',
                         stats)
        skills = response.xpath("//div[@class='ct-skills__item']")
        loader.add_value('skills',
                         skills)
        attacks = response.xpath("//div[@class='ct-attack-table__content']/div")
        loader.add_value('attacks',
                         attacks)
        yield loader.load_item()