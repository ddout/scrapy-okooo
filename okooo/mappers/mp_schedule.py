# -*- coding: utf-8 -*-
from pgsqlwares import Pgsql


class ScheduleMapper(object):
    __pgsql = None

    def __init__(self):
        self.__pgsql = Pgsql()

    def save(self, **kwargs):
        old = self.getById(kwargs["id"])
        if old == None:
            sql = "insert into okooo.schedule(id, area, country, match_name, sch_idx, " \
                  "sch_url, sch_name, sch_type, sch_group, sch_trun) " \
                  " values(%(id)s, %(area)s, %(country)s, %(match_name)s, %(sch_idx)s, " \
                  "%(sch_url)s, %(sch_name)s, %(sch_type)s, %(sch_group)s, %(sch_trun)s);"
            self.__pgsql.insertObj(sql, **kwargs)

    def getById(self, id):
        sql = "select * from okooo.schedule where id=%(id)s;"
        obj = self.__pgsql.getObj(sql, **{"id": id})
        return obj

    def getList(self):
        pass
