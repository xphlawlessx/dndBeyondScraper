import scrapy
from scrapy.loader import ItemLoader
from dndBeyond.items import DndbeyondItem
import os
import json

class CharacterSpider(scrapy.Spider):
    name = "character"
    start_urls = ["https://www.dndbeyond.com/profile/Further_Reading/characters/6268603"]

    def start_requests(self):
        # Note - requires a splashy image running on a docker
        # see https://blog.scrapinghub.com/2015/03/02/handling-javascript-in-scrapy-with-splash
        req_url = "http://localhost:8050/render.html"
        for url in self.start_urls:
            body = json.dumps({
                "url": url,
                "wait": 5,
            })
            headers = {'Content-Type': 'application/json'}
            yield scrapy.Request(req_url, self.parse, method='POST',
                                 body=body, headers=headers)

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