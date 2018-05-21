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
    match_name = scrapy.Field()
    match_url = scrapy.Field()


class ScheduleInfo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    area = scrapy.Field()
    country = scrapy.Field()
    match_name = scrapy.Field()
    sch_idx = scrapy.Field()
    sch_url = scrapy.Field()
    sch_name = scrapy.Field()
    sch_type = scrapy.Field()
    sch_group = scrapy.Field()
    sch_trun = scrapy.Field()
    schedule_teams = scrapy.Field()
