# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MatchInfo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    area = scrapy.Field()
    country = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()


class OkoooItem2(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name2 = scrapy.Field()
