# -*- coding: utf-8 -*-
import copy

import scrapy
from scrapy import signals

from okooo.mappers.mp_commons import SpiderStatusMapper
from okooo.mappers.mp_data_update import DataUpdateMapper
from okooo.mappers.mp_play import PlayMapper


class PlayExt(object):
    def __init__(self, settings):
        print("play ext init............")
        self.__spiderStatusMapper = SpiderStatusMapper()
        self.__dataUpdateMapper = DataUpdateMapper()
        self.__spider_name1 = ["sp_palys_odd", "sp_palys_even"]
        self.__spider_name2 = ["spiders_sch_plays_update"]
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
        if spider.name in self.__spider_name1 or spider.name in self.__spider_name2:
            self.__playMapper = PlayMapper()
            # 读取记录当前状态
            status = self.__spiderStatusMapper.loadSpiderStatus(spider_name=spider.name)
            page = 0
            if status != None:
                page = status.get("page", 0)
            else:
                if spider.name == "sp_palys_odd":
                    page = 1
                if spider.name == "sp_palys_even":
                    page = 0
            spider.page = page

    def spider_closed(self, spider):
        spider.log("opened spider %s" % spider.name)

    def spider_idle(self, spider):
        spider.log("opened spider %s" % spider.name)

        if (spider.name in self.__spider_name1) and spider.cookie_jar != -1:
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
        # 没有比赛的赛季
        if (spider.name in self.__spider_name2) and spider.cookie_jar != -1:
            # 从db中读取数据
            page = spider.page
            #
            sch_list = self.__dataUpdateMapper.getDotHavePlaySchList(limit=10, page=page)
            if sch_list != None and len(sch_list) > 0:
                spider.page = page + 1
                for sch in sch_list:
                    play_url = spider.base_url + sch["sch_url"]
                    playInfo = copy.deepcopy(sch)
                    res = scrapy.Request(url=play_url, headers=spider.headers,
                                         meta={'cookiejar': spider.cookie_jar, "playInfoObj": playInfo},
                                         callback=spider.parse_oddsList)
                    spider.crawler.engine.crawl(res, spider)
            else:
                # 比赛详情更新
                playpage = spider.playpage
                #
                play_list = self.__dataUpdateMapper.getModifyPlayList(limit=10, page=playpage)
                if play_list != None and len(play_list) > 0:
                    spider.playpage = playpage + 1
                    for play in play_list:
                        play_url = spider.base_url + "/soccer/match/" + str(play["id"]) + "/odds/"
                        playInfo = copy.deepcopy(play)
                        res = scrapy.Request(url=play_url, headers=spider.headers,
                                             meta={'cookiejar': spider.cookie_jar, "playInfoObj": playInfo},
                                             callback=spider.parse_playInfo)
                        spider.crawler.engine.crawl(res, spider)
