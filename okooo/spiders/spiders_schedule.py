# -*- coding: utf-8 -*-
import copy
import json
import re
import time

import scrapy
import logging

# 解析赛事
from parsel import Selector

from okooo.items import MatchInfo, ScheduleInfo

# 赛季
from okooo.mappers.mp_match import MatchMapper


class okoooSpider(scrapy.Spider):
    name = "sp_schedule"
    allowed_domains = ["www.okooo.com"]

    headers = {
        "Accept": "text/html, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.okooo.com",
        "Pragma": "no-cache",
        "Referer": "http://www.okooo.com/soccer/",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

    # start_urls = []
    base_url = "http://www.okooo.com"
    index_url = "http://www.okooo.com"  # ""http://www.okooo.com/soccer/league/1/"
    #
    __matchMapper = None

    # 起始加载获取验证码图片
    def start_requests(self):
        logging.debug("加载页面,固化cookies..........")
        self.__matchMapper = MatchMapper()
        return [
            scrapy.Request(url=self.index_url, headers=self.headers,
                           meta={'cookiejar': 1}, callback=self.loop_start_url)]

        #test
        #
        # match_url = "http://www.okooo.com/soccer/league/18/schedule/10089/1-2-46/"
        # scheduleInfo = {"area": "test", "country": "test", "match_name": "test"}
        # return [
        #     scrapy.Request(url=match_url, headers=self.headers,
        #                    meta={'cookiejar': 1, "scheduleInfoObj": scheduleInfo},
        #                    callback=self.parse_schList)]

    # 增量加载
    def loop_start_url(self, response):
        # 从db中读取数据
        page = 0
        while True:
            match_list = self.__matchMapper.getList(limit=10, page=page)
            if match_list == None or len(match_list) == 0:
                break
            page = page + 1
            for match in match_list:
                match_url = self.base_url + match["match_url"]
                scheduleInfo = {"area": match["area"], "country": match["country"], "match_name": match["match_name"]}
                yield scrapy.Request(url=match_url, headers=self.headers,
                                     meta={'cookiejar': 1, "scheduleInfoObj": scheduleInfo},
                                     callback=self.parse_schList)

    # 主要解析方法
    def parse_schList(self, response):
        # 解析赛季列表
        sch_list = response.css("div.LeftLittleWidth div.LotteryList_Data ul li a").extract()
        idx = len(sch_list)
        for m in sch_list:
            #
            scheduleInfo = copy.deepcopy(response.meta["scheduleInfoObj"])
            #
            target_sel = Selector(text=m)
            name = target_sel.css("::text").extract_first().strip()
            url = target_sel.xpath("//@href").extract_first().strip()
            id_parse = re.findall("schedule/(\d+)/", url)
            if len(id_parse) == 0:
                continue
            id = id_parse[0]
            scheduleInfo["id"] = id
            scheduleInfo["sch_name"] = name
            scheduleInfo["sch_url"] = url
            scheduleInfo["sch_idx"] = idx
            idx = idx - 1
            #
            self.headers["Referer"] = response.url
            yield scrapy.Request(url=self.base_url + url, headers=self.headers,
                                 meta={'cookiejar': 1, "scheduleInfoObj": scheduleInfo},
                                 callback=self.parse_type)

    #
    def parse_type(self, response):
        # 解析比赛类型
        logging.debug(response.url)
        sch_type = response.css("div#m_id").extract()
        type_len = len(sch_type)
        if type_len == 0:
            # 没有类型
            scheduleInfo = copy.deepcopy(response.meta["scheduleInfoObj"])
            logging.debug(scheduleInfo)
            scheduleInfo["sch_type"] = "无"
            scheduleInfo["id"] = response.meta["scheduleInfoObj"]["id"] + "_0"
            yield scrapy.Request(url=buildRandomUrl(response.url), headers=self.headers,
                                 meta={'cookiejar': 1, "scheduleInfoObj": scheduleInfo},
                                 callback=self.parse_group)
        else:
            for type in sch_type:
                #
                scheduleInfo = copy.deepcopy(response.meta["scheduleInfoObj"])
                logging.debug(scheduleInfo)
                #
                logging.debug("sch_type html: " + type)
                sch_type_sel = Selector(text=type)
                name = sch_type_sel.css("a::text").extract_first()
                if name == None or name == "" or name == "null":
                    continue
                url = sch_type_sel.xpath("//a/@href").extract_first()
                scheduleInfo["sch_type"] = name
                scheduleInfo["id"] = response.meta["scheduleInfoObj"]["id"] + "_" + name
                #
                yield scrapy.Request(url=self.base_url + url, headers=self.headers,
                                     meta={'cookiejar': 1, "scheduleInfoObj": scheduleInfo},
                                     callback=self.parse_group)

    #
    def parse_group(self, response):
        # 解析比赛分组
        logging.debug(response.url)
        sch_group = response.css("div.tabWidth").extract()
        if len(sch_group) <= 1:
            # 无分组
            #
            scheduleInfo = copy.deepcopy(response.meta["scheduleInfoObj"])
            logging.debug(scheduleInfo)
            #
            scheduleInfo["sch_group"] = "无"
            scheduleInfo["id"] = response.meta["scheduleInfoObj"]["id"] + "_0"
            yield scrapy.Request(url=buildRandomUrl(response.url), headers=self.headers,
                                 meta={'cookiejar': 1, "scheduleInfoObj": scheduleInfo},
                                 callback=self.parse_trun)
        else:
            # 有分组
            groups = Selector(text=sch_group[1]).css("a").extract()
            for g in groups:
                #
                scheduleInfo = copy.deepcopy(response.meta["scheduleInfoObj"])
                logging.debug(scheduleInfo)
                #
                g_sel = Selector(text=g)
                name = g_sel.css("a::text").extract_first()
                url = g_sel.xpath("//@href").extract_first()
                scheduleInfo["sch_group"] = name
                scheduleInfo["id"] = response.meta["scheduleInfoObj"]["id"] + "_" + name
                yield scrapy.Request(url=self.base_url + url, headers=self.headers,
                                     meta={'cookiejar': 1, "scheduleInfoObj": scheduleInfo},
                                     callback=self.parse_trun)

    #
    def parse_trun(self, response):
        # 解析比赛轮次和球队
        logging.debug(response.url)
        sch_trun = response.css("table.linkblock a.OddsLink").extract()
        # schInfo["schedule_teams"] = schInfo["id"]
        if len(sch_trun) == 0:
            # 无轮次
            #
            scheduleInfo = copy.deepcopy(response.meta["scheduleInfoObj"])
            logging.debug(scheduleInfo)
            #
            schInfo = ScheduleInfo()
            schInfo["id"] = scheduleInfo["id"]
            schInfo["area"] = scheduleInfo["area"]
            schInfo["country"] = scheduleInfo["country"]
            schInfo["match_name"] = scheduleInfo["match_name"]
            schInfo["sch_idx"] = scheduleInfo["sch_idx"]
            schInfo["sch_name"] = scheduleInfo["sch_name"]
            schInfo["sch_type"] = scheduleInfo["sch_type"]
            schInfo["sch_group"] = scheduleInfo["sch_group"]
            schInfo["sch_trun"] = "无"
            schInfo["id"] = response.meta["scheduleInfoObj"]["id"] + "_0"
            schInfo["sch_url"] = response.url.replace(self.base_url, "")
            yield schInfo
        else:
            # 有轮次
            for t in sch_trun:

                odds_sel = Selector(text=t)
                trun_name = odds_sel.css("a::text").extract_first();
                if trun_name == None or trun_name.strip() == "":
                    trun_name = odds_sel.css("a b::text").extract_first();
                    if trun_name == None or trun_name.strip() == "":
                        continue
                trun_name = trun_name.strip()
                tmp_name = trun_name.encode("utf-8")
                if tmp_name == None or tmp_name == "" or tmp_name == "全部":
                    continue
                #
                scheduleInfo = copy.deepcopy(response.meta["scheduleInfoObj"])
                logging.debug(scheduleInfo)
                #
                schInfo = ScheduleInfo()
                schInfo["id"] = scheduleInfo["id"]
                schInfo["area"] = scheduleInfo["area"]
                schInfo["country"] = scheduleInfo["country"]
                schInfo["match_name"] = scheduleInfo["match_name"]
                schInfo["sch_idx"] = scheduleInfo["sch_idx"]
                schInfo["sch_name"] = scheduleInfo["sch_name"]
                schInfo["sch_type"] = scheduleInfo["sch_type"]
                schInfo["sch_group"] = scheduleInfo["sch_group"]
                schInfo["sch_trun"] = trun_name
                schInfo["id"] = response.meta["scheduleInfoObj"]["id"] + "_" + trun_name
                schInfo["sch_url"] = odds_sel.xpath("//@href").extract_first().strip()
                yield schInfo


def buildRandomUrl(url):
    if url.find("?") != -1:
        return url + "&t2=" + str(int(round(time.time() * 1000)))
    else:
        return url + "?t=" + str(int(round(time.time() * 1000)))
