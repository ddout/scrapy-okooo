# -*- coding: utf-8 -*-
from scrapy import cmdline

# test run
# 赛事-赛季列表
cmdline.execute("scrapy crawl sp_schedule_update".split())