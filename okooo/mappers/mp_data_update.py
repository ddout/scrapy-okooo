# -*- coding: utf-8 -*-
from pgsqlwares import Pgsql


class DataUpdateMapper(object):
    __pgsql = None

    def __init__(self):
        self.__pgsql = Pgsql()



    def existsSchedule(self, **kwargs):
        sql = """
                select count(1) cnt from okooo.schedule
                where area=%(area)s
                  and country=%(country)s
                  and match_name=%(match_name)s
                  and sch_idx='%(sch_idx)s'
              """
        match = self.__pgsql.getObj(sql, **kwargs)
        return match

    def getList(self, page=0, limit=10):
        sql = "select id, area, country, match_name, match_url from okooo.match " \
              "order by to_number(id,'9999999') asc " \
              "limit %(limit)s offset %(offset)s ;"
        #
        v_offset = page * limit
        v_limit = limit
        #
        params = {"offset": v_offset, "limit": v_limit}
        return self.__pgsql.getAll(sql, **params)
