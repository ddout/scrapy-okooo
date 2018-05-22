# -*- coding: utf-8 -*-
from scrapy import cmdline

# test run
# 首页--国家-赛事列表
cmdline.execute("scrapy crawl sp_match".split())
# 赛事-赛季列表
#cmdline.execute("scrapy crawl sp_schedule".split())
