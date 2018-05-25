# -*- coding: utf-8 -*-
import copy

import scrapy
from scrapy import signals

from okooo.mappers.mp_commons import SpiderStatusMapper
from okooo.mappers.mp_play import PlayMapper


class PlayExt(object):
    def __init__(self, settings):
        print("play ext init............")
        self.__spiderStatusMapper = SpiderStatusMapper()
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
        if spider.name == "sp_palys_odd" or spider.name == "sp_palys_even":
            self.__playMapper = PlayMapper()
            # 读取记录当前状态
            status = self.__spiderStatusMapper.loadSpiderStatus(spider_name=spider.name)
            page = 0
            if status != None:
                page = status.get("page", 0)
            if spider.name == "sp_palys_odd":
                page = 1
            if spider.name == "sp_palys_even":
                page = 0
            spider.page = page

    def spider_closed(self, spider):
        spider.log("opened spider %s" % spider.name)

    def spider_idle(self, spider):
        spider.log("opened spider %s" % spider.name)

        if (spider.name == "sp_palys_odd" or spider.name == "sp_palys_even") and spider.cookie_jar != -1:
            # 从db中读取数据
            page = spider.page
            # 记录当前状态
            self.__spiderStatusMapper.saveSpiderStatus(spider_name=spider.name, page=page)
            #
            sch_list = self.__playMapper.getSchList(limit=10, page=page)
            if sch_list != None and len(sch_list) > 0:
                spider.page = page + 2
                for sch in sch_list:
                    play_url = spider.base_url + sch["sch_url"]
                    playInfo = copy.deepcopy(sch)
                    res = scrapy.Request(url=play_url, headers=spider.headers,
                                         meta={'cookiejar': spider.cookie_jar, "playInfoObj": playInfo},
                                         callback=spider.parse_oddsList)
                    spider.crawler.engine.crawl(res, spider)
