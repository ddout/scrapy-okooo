# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from okooo.items import MatchInfo, ScheduleInfo
from okooo.mappers.mp_match import MatchMapper


class OkoooPipeline(object):
    __matchMapper = None

    def __init__(self):
        self.__matchMapper = MatchMapper()

    def process_item(self, item, spider):
        # 赛事
        if isinstance(item, MatchInfo):
            if item["match_name"] == None or item["match_name"] == "" or item["match_name"] == "null":
                raise DropItem("this Match is not valiadate")
            # save obj
            self.__matchMapper.save(**dict(item))

            return item

        # 赛季轮次
        if isinstance(item, ScheduleInfo):
            if item["match_name"] == None or item["match_name"] == "" or item["match_name"] == "null":
                raise DropItem("this Match is not valiadate")
            # save obj
            print(item)

            return item
