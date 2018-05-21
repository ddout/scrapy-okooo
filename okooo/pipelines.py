# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from okooo.items import MatchInfo


class OkoooPipeline(object):
    def process_item(self, item, spider):
        # 赛事
        if isinstance(item, MatchInfo):
            print(item["id"])
            print(item["name"])
            print(item["url"])

            return item
