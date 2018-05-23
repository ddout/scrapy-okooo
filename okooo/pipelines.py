# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from okooo.items import MatchInfo, ScheduleInfo, PlayInfo
from okooo.mappers.mp_match import MatchMapper
from okooo.mappers.mp_play import PlayMapper
from okooo.mappers.mp_schedule import ScheduleMapper


class OkoooPipeline(object):
    __matchMapper = None
    __schMapper = None
    __playMapper = None

    def __init__(self):
        self.__matchMapper = MatchMapper()
        self.__schMapper = ScheduleMapper()
        self.__playMapper = PlayMapper()

    def process_item(self, item, spider):
        # 赛事match
        if isinstance(item, MatchInfo):
            if item["match_name"] == None or item["match_name"] == "" or item["match_name"] == "null":
                raise DropItem("this Match is not valiadate")
            # save obj
            self.__matchMapper.save(**dict(item))
            return item

        # 赛季轮次schedule
        if isinstance(item, ScheduleInfo):
            if item["id"] == None or item["id"] == "" or item["id"] == "null":
                raise DropItem("this Match is not valiadate")
            # save obj
            self.__schMapper.save(**dict(item))
            return item

        # 比赛详情play
        if isinstance(item, PlayInfo):
            if item["id"] == None or item["id"] == "" or item["id"] == "null":
                raise DropItem("this Play is not valiadate")
            # save obj
            self.__playMapper.save(**dict(item))
            return item
