# -*- coding: utf-8 -*-
import copy

import scrapy
from scrapy import signals

from okooo.mappers.mp_play import PlayMapper


class PlayExt(object):

    def __init__(self, settings):
        print("play ext init............")
        pass

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        return ext

    def spider_opened(self, spider):
        spider.log("opened spider %s" % spider.name)
        if spider.name == "sp_palys":
            self.__playMapper = PlayMapper()

    def spider_closed(self, spider):
        spider.log("opened spider %s" % spider.name)

    def spider_idle(self, spider):
        spider.log("opened spider %s" % spider.name)

        if spider.name == "sp_palys" and spider.cookie_jar == 1:
            # 从db中读取数据
            page = spider.page
            sch_list = self.__playMapper.getSchList(limit=10, page=page)
            if sch_list != None and len(sch_list) > 0:
                spider.page = page + 1
                for sch in sch_list:
                    play_url = spider.base_url + sch["sch_url"]
                    playInfo = copy.deepcopy(sch)
                    res = scrapy.Request(url=play_url, headers=spider.headers,
                                         meta={'cookiejar': spider.cookie_jar, "playInfoObj": playInfo}, callback=spider.parse_oddsList)
                    spider.crawler.engine.crawl(res, spider)
