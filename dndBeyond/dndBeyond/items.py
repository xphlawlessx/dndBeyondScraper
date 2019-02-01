# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


def mapStats(statResponses):
    """
    Split statResponses into dicts with required dat for each stat
    Args:
        statResponses (list): list of scrapy Responses

    Returns (dict): dictionary of the form {'stat':{'value': int,
                                                    'modifier': int}}

    """
    stats = {}
    for response in statResponses:
        statName = response.xpath("div/span[@class='ct-ability-summary__label']//text()").extract_first()
        statValue = response.xpath("div[@class='ct-ability-summary__primary']//text()").extract_first()
        if statValue in "-+":
            # primary and secondary flipped
            statValue = response.xpath("div[@class='ct-ability-summary__secondary']//text()").extract_first()
        modValue = getModifier(response)
        stats[statName] = {'value': statValue,
                       'modifier': modValue}

    yield stats

def mapSkills(skillResponses):
    """
    Split skillResponses into dicts with required dat for each stat
    Args:
        skillResponses (list): list of scrapy Responses

    Returns (dict): dictionary of the form {'stat':{'attribute': str,
                                                    'modifier': int}}

    """
    skills = {}
    for response in skillResponses:
        attribute = response.xpath("div[@class='ct-skills__col--stat']//text()").extract_first()
        skillName = response.xpath("div[@class='ct-skills__col--skill']//text()").extract_first()
        modValue = getModifier(response)
        skills[skillName] = {'attribute': attribute,
                         'modifier': modValue}

    yield skills

def mapAttacks(attackResponses):
    """
    Split attackResponses into dicts with required data for each attack
    dict will have 'hit' or 'save' fields depending on type of attack
    Args:
        attackResponses (list): list of scrapy Responses

    Returns (dict): dictionary of the form {'attackName':{'hit'/'save': int,
                                                          'damage': str}}

    """
    attacks = {}
    for attackResponse in attackResponses:
        name = attackResponse.xpath("div[@class='ct-combat-attack__name']//text()").extract_first()
        hitModiferResponse = attackResponse.xpath("div[@class='ct-combat-attack__action']")
        damage = attackResponse.xpath("div[@class='ct-combat-attack__damage']//text()").extract_first()
        try:
            hitModifer = getModifier(hitModiferResponse)
            attacks[name] = {'hit': hitModifer,
                             'damage': damage}
        except TypeError:
            saveDetails = attackResponse.xpath("div[@class='ct-combat-attack__action']//text()").extract()
            save = f"{saveDetails[0]} {saveDetails[1]}"
            attacks[name] = {'save': save,
                             'damage': damage}

    yield attacks

def getModifier(response):
    """
    Get the modifers from the response
    Args:
        response (Scrapy response): scrapy response representing a node for a specific attribute

    Returns (int): the modifer amount

    """
    modSymbol = response.xpath("div/span/span[@class='ct-signed-number__sign']//text()").extract_first()
    modAmount = response.xpath("div/span/span[@class='ct-signed-number__number']//text()").extract_first()
    print(response)
    return int(modSymbol + modAmount)


class DndbeyondItem(scrapy.Item):
    name = scrapy.Field(output_processor = TakeFirst())
    stats = scrapy.Field(input_processor = mapStats,
                        output_processor = TakeFirst())
    skills = scrapy.Field(input_processor = mapSkills,
                        output_processor = TakeFirst())
    attacks = scrapy.Field(input_processor = mapAttacks,
                        output_processor = TakeFirst())