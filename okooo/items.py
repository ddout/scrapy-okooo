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


class PlayInfo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    area = scrapy.Field()
    country = scrapy.Field()
    match_name = scrapy.Field()
    sch_name = scrapy.Field()
    sch_type = scrapy.Field()
    sch_group = scrapy.Field()
    sch_trun = scrapy.Field()
    #
    play_urls = scrapy.Field()
    play_time = scrapy.Field()
    team_home = scrapy.Field()
    team_vis = scrapy.Field()
    half_home = scrapy.Field()
    half_vis = scrapy.Field()
    full_home = scrapy.Field()
    full_vis = scrapy.Field()
    play_result = scrapy.Field()
    play_result_detail = scrapy.Field()
    odds_info = scrapy.Field()
