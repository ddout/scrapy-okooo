# -*- coding: utf-8 -*-
import json
import re

import scrapy
import logging

# 解析赛事
from parsel import Selector

from okooo.items import MatchInfo


class okoooSpider(scrapy.Spider):
    name = "sp_match"
    allowed_domains = ["www.okooo.com"]

    headers = {
        "Accept": "text/html, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.okooo.com",
        "Referer": "http://www.okooo.com/soccer/",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

    # start_urls = []
    index_url = "http://www.okooo.com/soccer/"

    # 起始加载获取验证码图片
    def start_requests(self):
        logging.debug("加载页面,固化cookies..........")
        return [
            scrapy.Request(url=self.index_url, headers=self.headers, meta={'cookiejar': 1}, callback=self.parse_index)]

    # 主要解析方法
    def parse_index(self, response):
        # 一共有四个
        # 欧洲
        match01 = response.css("div#Match01 div.MatchInfoListPic_L").extract()

        for m in match01:
            m_select = Selector(text=m)
            country = m_select.css("div.MatchInfoLogoName::text").extract_first("").strip()
            #
            toolbox = m_select.css("div.Toolbox div.MatchShowOff").extract()
            for m_name in toolbox:
                target_select = Selector(text=m_name)
                ##
                onclick_data = target_select.xpath("//@onclick").extract_first().strip()
                ##
                matchInfo = MatchInfo()
                matchInfo["id"] = re.findall("(\d+)", onclick_data)[0]
                matchInfo["area"] = "欧洲赛事"
                matchInfo["country"] = country
                matchInfo["match_name"] = target_select.css("::text").extract_first()
                matchInfo["match_url"] = onclick_data[13:len(onclick_data) - 3]
                #
                yield matchInfo

        # 美洲
        match02 = response.css("div#Match02 div.MatchInfoListPic_L").extract()
        for m in match02:

            m_select = Selector(text=m)
            country = m_select.css("div.MatchInfoLogoName::text").extract_first("").strip()
            #
            toolbox = m_select.css("div.Toolbox div.MatchShowOff").extract()
            for m_name in toolbox:
                target_select = Selector(text=m_name)
                ##
                onclick_data = target_select.xpath("//@onclick").extract_first().strip()
                matchInfo = MatchInfo()
                ##
                matchInfo["id"] = re.findall("(\d+)", onclick_data)[0]
                matchInfo["area"] = "美洲赛事"
                matchInfo["country"] = country
                matchInfo["match_name"] = target_select.css("::text").extract_first()
                matchInfo["match_url"] = onclick_data[13:len(onclick_data) - 3]
                #
                yield matchInfo
        # 亚洲
        match03 = response.css("div#Match03 div.MatchInfoListPic_L").extract()
        for m in match03:

            m_select = Selector(text=m)
            country = m_select.css("div.MatchInfoLogoName::text").extract_first("").strip()
            #
            toolbox = m_select.css("div.Toolbox div.MatchShowOff").extract()
            for m_name in toolbox:
                target_select = Selector(text=m_name)
                ##
                onclick_data = target_select.xpath("//@onclick").extract_first().strip()
                ##
                matchInfo = MatchInfo()
                matchInfo["id"] = re.findall("(\d+)", onclick_data)[0]
                matchInfo["area"] = "亚洲赛事"
                matchInfo["country"] = country
                matchInfo["match_name"] = target_select.css("::text").extract_first()
                matchInfo["match_url"] = onclick_data[13:len(onclick_data) - 3]
                #
                yield matchInfo
        # 洲际(杯赛)
        match04 = response.css("div#Match04 div.MatchInfoListPic_L").extract()
        for m in match04:

            m_select = Selector(text=m)
            country = m_select.css("div.MatchInfoLogoName::text").extract_first("").strip()
            #
            toolbox = m_select.css("div.Toolbox div.MatchShowOff").extract()
            for m_name in toolbox:
                target_select = Selector(text=m_name)
                ##
                onclick_data = target_select.xpath("//@onclick").extract_first().strip()
                ##
                matchInfo = MatchInfo()
                matchInfo["id"] = re.findall("(\d+)", onclick_data)[0]
                matchInfo["area"] = "洲际赛事"
                matchInfo["country"] = country
                matchInfo["match_name"] = target_select.css("::text").extract_first()
                matchInfo["match_url"] = onclick_data[13:len(onclick_data) - 3]
                #
                yield matchInfo
