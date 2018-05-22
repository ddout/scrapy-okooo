# -*- coding: utf-8 -*-
import json
import random

import scrapy
import logging
import os

# 解析比赛
from scrapy import Selector

from okooo.items import PlayInfo


class okoooSpider(scrapy.Spider):
    name = "sp_palys"
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

    # http://www.okooo.com/soccer/league/777/schedule/11958/1-6230-11/
    # http://www.okooo.com/soccer/league/18/schedule/10090/1-2-1/
    base_url = "http://www.okooo.com"
    index_url = "/soccer/league/18/schedule/10090/1-2-1/"

    # 起始加载获取验证码图片
    def start_requests(self):
        logging.debug("起始加载获取验证码图片..........")
        captcha_url = "http://www.okooo.com/I/?method=ok.user.settings.authcodepic&r0.2911857041554329"
        return [
            scrapy.Request(url=captcha_url, headers=self.headers, meta={'cookiejar': 1}, callback=self.parser_captcha)]

    def parser_captcha(self, response):
        with open('captcha.jpg', 'wb') as f:
            f.write(response.body)
            f.close()
        print(u"请到 {0} 目录找到captcha.jpg 手动输入".format(os.path.abspath('captcha.jpg')))

        captcha_val = raw_input("please input the captcha >>") + ""

        print(captcha_val)

        post_url = "http://www.okooo.com/I/?method=user.user.userlogin"
        post_data = {
            "UserName": "he56789",
            "PassWord": "he567890",
            "LoginType": "okooo",
            "RememberMe": "0",
            "AuthType": "okooo",
            "AuthCode": captcha_val
        }
        return [scrapy.FormRequest(url=post_url, formdata=post_data, headers=self.headers,
                                   meta={'cookiejar': response.meta['cookiejar']}, callback=self.check_login)]

    def check_login(self, response):
        # {"user_userlogin_response":{"errorno":6,"LoginErrorNo":8,"LoginErrorTime":5,"error":-2}}
        print(response.text)
        js = json.loads(response.text)
        if 'user_userlogin_response' in js and 'UserID' in js['user_userlogin_response']:
            print("ok-----okooo is login success!!!!")
            return [
                scrapy.Request(url=self.base_url + self.index_url, headers=self.headers,
                               meta={'cookiejar': response.meta['cookiejar']},
                               # dont_filter=True, callback=self.loop_start_url)]
                               dont_filter=True, callback=self.parse_oddsList)]
        else:
            if "msg" in js['user_userlogin_response']:
                print(js['user_userlogin_response']['msg'])

    # 增量加载
    def loop_start_url(self, response):
        # 从db中读取数据
        page = 0
        # while True:
        #     match_list = self.__matchMapper.getList(limit=10, page=page)
        #     if match_list == None or len(match_list) == 0:
        #         break
        #     page = page + 1
        #     for match in match_list:
        #         match_url = self.base_url + match["match_url"]
        #         playInfo = {"area": match["area"], "country": match["country"],
        #                         "match_name": match["match_name"]}
        #         yield scrapy.Request(url=match_url, headers=self.headers,
        #                              meta={'cookiejar': response.meta['cookiejar'], "playInfoObj": playInfo},
        #                              callback=self.parse_schList)

    # 解析列表
    def parse_oddsList(self, response):
        # #team_fight_table tr[class!=LotteryListTitle
        play_list = response.css("#team_fight_table tr:not(.LotteryListTitle)").extract()
        for p in play_list:
            play_sel = Selector(text=p)
            # 取matchid
            matchid = play_sel.xpath("//@matchid").extract_first()
            # 取odds_url
            odds_url = "/soccer/match/" + matchid + "/odds/"
            playInfo = {"area": "", "country": "", "match_name": ""}
            yield scrapy.Request(url=self.base_url + odds_url, headers=self.headers,
                                 meta={'cookiejar': response.meta['cookiejar'], "playInfoObj": playInfo},
                                 callback=self.parse_playInfo)

    # 解析比赛数据
    def parse_playInfo(self, response):
        play = PlayInfo()
        # 赛事时间
        play["play_time"] = response.css("div.qbox_1 div.qbx_2 p").extract_first()
        # 主队
        play["team_home"] = response.css("#matchTeam div.qpai_zi").extract_first()
        # 客队
        play["team_vis"] = response.css("#matchTeam div.qpai_zi_1").extract_first()
        #
        score_half = response.css("div.jifen_dashi p").extract_first()
        if score_half != None:
            # 半:1-1
            score_half_arr = score_half.strip().replace("半:", "").split("-")
            # 比分半场主
            play["half_home"] = score_half_arr[0]
            # 比分半场客
            play["half_home"] = score_half_arr[1]
        # $("#matchTeam div.vs span")[0]
        score_full = response.css("#matchTeam div.vs span").extract()
        if score_full == None:
            # 比分全场主
            play["full_home"] = None
            # 比分全场客
            play["full_vis"] = None
            # 赛事结果
            play["play_result"] = None
        else:
            # 比分全场主
            play["full_home"] = Selector(text=score_full[0]).css("::text").extract_first().strip()
            # 比分全场客
            play["full_vis"] = Selector(text=score_full[1]).css("::text").extract_first().strip()
            # 赛事结果
            play["play_result"] = None
        #

        # 指数详情-额外的请求
        print(play)
