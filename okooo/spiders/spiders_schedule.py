# -*- coding: utf-8 -*-
import json
import re

import scrapy
import logging

# 解析赛事
from parsel import Selector

from okooo.items import MatchInfo, ScheduleInfo


# 赛季
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
    index_url = "http://www.okooo.com/soccer/league/1/"

    # 起始加载获取验证码图片
    def start_requests(self):
        logging.debug("加载页面,固化cookies..........")
        scheduleInfo = {"area": "area", "country": "country", "match_name": "match_name"}
        return [
            scrapy.Request(url=self.index_url, headers=self.headers,
                           meta={'cookiejar': 1, "scheduleInfo": scheduleInfo}, callback=self.parse_index)]

    # 主要解析方法
    def parse_index(self, response):
        # 解析赛季列表
        #
        scheduleInfo = response.meta["scheduleInfo"]
        #
        sch_list = response.css("div.LeftLittleWidth div.LotteryList_Data ul li a").extract()
        idx = len(sch_list)
        for m in sch_list:
            target_sel = Selector(text=m)
            name = target_sel.css("::text").extract_first().strip()
            tmp_name = name.encode("utf-8")
            if tmp_name == "积 分 榜" or tmp_name == "射手榜" or tmp_name == "球员信息统计" or tmp_name == "赛季盘口查询":
                continue
            url = target_sel.xpath("//@href").extract_first().strip()
            id = re.findall("schedule/(\d+)/", url)[0]
            scheduleInfo["id"] = id
            scheduleInfo["sch_name"] = name
            scheduleInfo["sch_url"] = url
            scheduleInfo["sch_idx"] = idx
            idx = idx - 1
            #
            self.headers["Referer"] = response.url
            yield scrapy.Request(url=self.base_url + url, headers=self.headers,
                                 meta={'cookiejar': 1, "scheduleInfo": scheduleInfo},
                                 callback=self.parse_type)

    #
    def parse_type(self, response):
        # 解析比赛类型
        logging.debug(response.url)
        #
        scheduleInfo = response.meta["scheduleInfo"]
        logging.debug(scheduleInfo)
        sch_type = response.css("div#m_id").extract()
        type_len = len(sch_type)
        if type_len == 0:
            scheduleInfo["sch_type"] = "无"
            yield scrapy.Request(url=response.url, headers=self.headers,
                                 meta={'cookiejar': 1, "scheduleInfo": scheduleInfo},
                                 callback=self.parse_group)
            logging.debug(scheduleInfo["sch_type"])
        else:
            for type in sch_type:
                logging.debug("sch_type html: " + type)
                sch_type_sel = Selector(text=type)
                name = sch_type_sel.css("a::text").extract_first()
                url = sch_type_sel.xpath("//a/@href").extract_first()
                scheduleInfo["sch_type"] = name
                #
                yield scrapy.Request(url=self.base_url + url, headers=self.headers,
                                     meta={'cookiejar': 1, "scheduleInfo": scheduleInfo},
                                     callback=self.parse_group)

    #
    def parse_group(self, response):
        # 解析比赛分组
        logging.debug(response.url)
        #
        scheduleInfo = response.meta["scheduleInfo"]
        logging.debug(scheduleInfo)
        sch_group = response.css("div.tabWidth").extract()
        if len(sch_group) <= 1:
            # 无分组
            scheduleInfo["sch_group"] = "无"
            yield scrapy.Request(url=response.url, headers=self.headers,
                                 meta={'cookiejar': 1, "scheduleInfo": scheduleInfo},
                                 callback=self.parse_trun)
        else:
            # 有分组
            groups = Selector(text=sch_group[1]).css("a").extract()
            for g in groups:
                g_sel = Selector(text=g)
                name = g_sel.css("a::text").extract_first()
                url = g_sel.xpath("//@href").extract_first()
                scheduleInfo["sch_group"] = name
                yield scrapy.Request(url=self.base_url + url, headers=self.headers,
                                     meta={'cookiejar': 1, "scheduleInfo": scheduleInfo},
                                     callback=self.parse_trun)

    #
    def parse_trun(self, response):
        # 解析比赛轮次和球队
        logging.debug(response.url)
        #
        scheduleInfo = response.meta["scheduleInfo"]
        logging.debug(scheduleInfo)
        sch_trun = response.css("table.linkblock a.OddsLink").extract()
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

        # schInfo["schedule_teams"] = schInfo["id"]
        if len(sch_trun) == 0:
            # 无轮次
            schInfo["sch_trun"] = "无"
            schInfo["id"] = scheduleInfo["id"] + "_0"
            schInfo["sch_url"] = response.url.replace(self.base_url)
            yield schInfo
        else:
            # 有轮次
            for t in sch_trun:
                odds_sel = Selector(text=t)
                trun_name = odds_sel.css("a::text").extract_first();
                if trun_name == None:
                    continue
                tmp_name = trun_name.encode("utf-8")
                if tmp_name == "" or tmp_name == None or tmp_name == "全部":
                    continue
                schInfo["sch_trun"] = trun_name
                schInfo["id"] = scheduleInfo["id"] + "_0"
                schInfo["sch_url"] = odds_sel.xpath("//@href").extract_first().strip()
                yield schInfo
