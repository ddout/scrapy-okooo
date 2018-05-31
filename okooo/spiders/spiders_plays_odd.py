# -*- coding: utf-8 -*-
import copy
import json

import scrapy
import logging
import os

# from scrapy.spiders import Rule
# from scrapy.linkextractors import LinkExtractor
from parsel import Selector

from okooo.app_configure import app_config
from okooo.img.img_yzm import getImgBase64, getYZM
from okooo.items import PlayInfo


# 解析比赛
class okoooPlayOddSpider(scrapy.Spider):
    name = "sp_palys_odd"
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

    # rules = (
    #     Rule(LinkExtractor(allow=(r'http://www.okooo.com/soccer/league/[0-9]+/schedule/*')),
    #          callback="parse_oddsList")
    # )

    # /soccer/league/777/schedule/11958/1-6230-11/
    # /soccer/league/18/schedule/10090/1-2-1/
    # /soccer/league/16/schedule/13542/1-3954/
    base_url = "http://www.okooo.com"

    cookie_jar = -1
    page = 0

    # 起始加载获取验证码图片

    def start_requests(self):
        logging.debug("起始加载获取验证码图片..........")
        captcha_url = "http://www.okooo.com/I/?method=ok.user.settings.authcodepic&r0.2911857041554329"
        yield scrapy.Request(url=captcha_url, headers=self.headers, meta={'cookiejar': 1}, callback=self.parser_captcha)

    def parser_captcha(self, response):
        with open('captcha_odd.jpg', 'wb') as f:
            f.write(response.body)
            f.close()
        # print(u"请到 {0} 目录找到captcha_odd.jpg 手动输入".format(os.path.abspath('captcha_odd.jpg')))

        # captcha_val = raw_input("please input the captcha >>") + ""
        captcha_val = getYZM(getImgBase64(os.path.abspath('captcha_odd.jpg')))

        print("yzm_odd:", captcha_val)

        img_path = os.path.abspath('captcha_odd.jpg')
        if os.path.exists(img_path):
            os.remove(img_path)
            print("captcha.jpg is removed!!!")

        post_url = "http://www.okooo.com/I/?method=user.user.userlogin"
        post_data = app_config["login_post_data"]
        post_data["AuthCode"] = captcha_val

        return [scrapy.FormRequest(url=post_url, formdata=post_data, headers=self.headers,
                                   meta={'cookiejar': response.meta['cookiejar']}, callback=self.check_login)]

    def check_login(self, response):
        # {"user_userlogin_response":{"errorno":6,"LoginErrorNo":8,"LoginErrorTime":5,"error":-2}}
        print(response.text)
        js = json.loads(response.text)
        if 'user_userlogin_response' in js and 'UserID' in js['user_userlogin_response']:
            print("ok-----okooo is login success!!!!")
            self.cookie_jar = response.meta['cookiejar']
        else:
            if "msg" in js['user_userlogin_response']:
                print(js['user_userlogin_response']['msg'])

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
            playInfo = copy.deepcopy(response.meta["playInfoObj"])
            playInfo["id"] = matchid
            playInfo["play_urls"] = odds_url
            yield scrapy.Request(url=self.base_url + odds_url, headers=self.headers,
                                 meta={'cookiejar': response.meta['cookiejar'], "playInfoObj": playInfo},
                                 callback=self.parse_playInfo)

    # 解析比赛数据
    def parse_playInfo(self, response):
        play = copy.deepcopy(response.meta["playInfoObj"])
        # 赛事id---轮次 由上层传入
        # url
        play["play_urls"] = response.url
        # 赛事时间
        time_str = response.css("div.qbox_1 div.qbx_2 p::text").extract_first()
        if time_str == None or time_str.encode("utf-8") == "延期":
            play["play_time"] = None
            if time_str.encode("utf-8") == "延期":
                play["﻿play_result_detail"] = "延期"
        else:
            time_year = time_str.split("-")[0]
            if int(time_year) >= 1 and int(time_year) < 30:
                time_str = "20" + time_str
            else:
                time_str = "19" + time_str
            time_str = time_str[0:10] + " " + time_str[11:]
            play["play_time"] = time_str

        # 主队
        play["team_home"] = response.css("#matchTeam div.qpai_zi::text").extract_first()
        # 客队
        play["team_vis"] = response.css("#matchTeam div.qpai_zi_1::text").extract_first()
        #
        score_half = response.css("div.jifen_dashi p").extract_first()
        if score_half != None:
            score_half_p = Selector(text=score_half).xpath("//p/text()").extract_first()
            if score_half_p != None:
                score_half = score_half_p
            if score_half != None:
                # 半:1-1
                score_half_arr = score_half.strip()[2:].split(" ")[0].split("-")
                # 比分半场主
                play["half_home"] = score_half_arr[0]
                # 比分半场客
                play["half_vis"] = score_half_arr[1]
            else:
                # 比分半场主
                play["half_home"] = None
                # 比分半场客
                play["half_vis"] = None
        # $("#matchTeam div.vs span")[0]
        score_full = response.css("#matchTeam div.vs span").extract()
        if score_full == None or len(score_full) == 0:
            # 比分全场主
            play["full_home"] = None
            # 比分全场客
            play["full_vis"] = None
            # 赛事结果
            play["play_result"] = None
        else:
            # 比分全场主
            play["full_home"] = int(Selector(text=score_full[0]).css("::text").extract_first().strip())
            # 比分全场客
            play["full_vis"] = int(Selector(text=score_full[1]).css("::text").extract_first().strip())
            # 赛事结果
            if play["full_home"] == play["full_vis"]:
                play["play_result"] = 1
            else:
                if play["full_home"] > play["full_vis"]:
                    play["play_result"] = 3
                else:
                    play["play_result"] = 0

        #
        # 指数详情-额外的请求
        # /soccer/match/954629/odds/ajax/?page=0&trnum=5&companytype=BigBooks&type=1
        # /soccer/match/954629/odds/ajax/?page=0&trnum=5&companytype=AuthoriteBooks&type=1
        odds_url = "/soccer/match/{0}/odds/ajax/?page=0&trnum=5&companytype=AuthoriteBooks&type=1".format(play["id"])
        return [scrapy.Request(url=self.base_url + odds_url, headers=self.headers,
                               meta={'cookiejar': response.meta['cookiejar'], "playInfoObj": play},
                               callback=self.parse_oddsInfo)]

    def parse_oddsInfo(self, response):
        script_str = response.xpath("//script").extract_first()
        # print(script_str)
        odds_json_str = script_str[
                        script_str.index("var data_str = '") + 15: script_str.index("var static_str =")].strip()[1:-2]
        playObj = response.meta["playInfoObj"]
        play = PlayInfo()
        play["odds_info"] = odds_json_str
        play["id"] = playObj.get("id")
        play["area"] = playObj.get("area")
        play["country"] = playObj.get("country")
        play["match_name"] = playObj.get("match_name")
        play["sch_name"] = playObj.get("sch_name")
        play["sch_type"] = playObj.get("sch_type")
        play["sch_group"] = playObj.get("sch_group")
        play["sch_trun"] = playObj.get("sch_trun")
        #
        play["play_urls"] = playObj.get("play_urls")
        play["play_time"] = playObj.get("play_time")
        play["team_home"] = playObj.get("team_home")
        play["team_vis"] = playObj.get("team_vis")
        play["half_home"] = playObj.get("half_home")
        play["half_vis"] = playObj.get("half_vis")
        play["full_home"] = playObj.get("full_home")
        play["full_vis"] = playObj.get("full_vis")
        play["play_result"] = playObj.get("play_result")
        play["play_result_detail"] = playObj.get("play_result_detail")
        #
        yield play
