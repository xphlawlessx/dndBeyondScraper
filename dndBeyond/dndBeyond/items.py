# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


def mapStats(statList):
    statsChunks = [statList[x:x + 5] for x in range(0, len(statList), 5)]
    stats = {}
    for chunk in statsChunks:
        stat = chunk[0]
        statValue = chunk[2]
        modValue = int(chunk[-2] + chunk[-1])
        stats[stat] = {'value': statValue,
                       'modifier': modValue}

    yield stats

class DndbeyondItem(scrapy.Item):
    name = scrapy.Field(output_processor = TakeFirst())
    stats = scrapy.Field(input_processor = mapStats,
                        output_processor = TakeFirst())