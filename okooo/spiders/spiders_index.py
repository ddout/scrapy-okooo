# -*- coding: utf-8 -*-
import json
import random

import scrapy
import logging
import os


class okoooSpider(scrapy.Spider):
    name = "sp_index"
    allowed_domains = ["www.okooo.com"]

    Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"

    headers = {
        "Accept": "text/html, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.okooo.com",
        "Referer": "http://www.okooo.com/soccer/",
        "X-Requested-With": "XMLHttpRequest",
        'User-Agent': Agent
    }

    # start_urls = ["http://www.okooo.com/soccer/match/1023200/odds/ajax/?page=0&trnum=0&companytype=BaijiaBooks&type=0"]
    start_urls = []
    index_url = "http://www.okooo.com/soccer/"

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
            # for url in self.start_urls:
            #     request = scrapy.Request(url=url, headers=self.headers, meta={'cookiejar': response.meta['cookiejar']},
            #                              dont_filter=True)
            #     # 传递参数
            #     request.meta["myparam"] = [{"a": "第一个", "b": "第二个"}]
            #     yield request
            metaData = {'cookiejar': response.meta['cookiejar'], 'myparam': [{"a": "第一个", "b": "第二个"}]}
            return [scrapy.Request(url=self.index_url, headers=self.headers, meta=metaData,
                                   dont_filter=True, callback=self.parse_index)]
        else:
            if "msg" in js['user_userlogin_response']:
                print(js['user_userlogin_response']['msg'])

    # 主要解析方法
    def parse_index(self, response):
        # print(response.body.decode(response.encoding))
        print(response.encoding)
        parm = response.meta["myparam"]
        print("解析咯:")
        print(parm)
        title = response.css("script").extract()
        # print(title)
        for t in zip(title):
            for i in t:
                # print(i)
                pass
