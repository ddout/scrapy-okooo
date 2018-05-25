# -*- coding: utf-8 -*-
from scrapy import cmdline

# 解析比赛
cmdline.execute("scrapy crawl sp_palys_odd".split())