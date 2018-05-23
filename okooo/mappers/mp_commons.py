# -*- coding: utf-8 -*-
from pgsqlwares import Pgsql


class SpiderStatusMapper(object):
    __pgsql = None

    def __init__(self):
        self.__pgsql = Pgsql()

    def saveSpiderStatus(self, spider_name, page):
        old = self.loadSpiderStatus(spider_name)
        if old == None:
            sql = "insert into okooo.spider_page_status" \
                  "(spider_name, page)" \
                  " values(%(spider_name)s, %(page)s);"
            self.__pgsql.insertObj(sql, **{"spider_name": spider_name, "page": page})
        else:
            sql = " update okooo.spider_page_status" \
                  " set page=%(page)s" \
                  " where spider_name=%(spider_name)s;"
            self.__pgsql.modifyObj(sql, **{"spider_name": spider_name, "page": page})

    def loadSpiderStatus(self, spider_name):
        sql = "select * from okooo.spider_page_status where spider_name=%(spider_name)s;"
        obj = self.__pgsql.getObj(sql, **{"spider_name": spider_name})
        return obj
