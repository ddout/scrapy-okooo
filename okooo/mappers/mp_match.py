# -*- coding: utf-8 -*-
from pgsqlwares import Pgsql


class MatchMapper(object):
    __pgsql = None

    def __init__(self):
        self.__pgsql = Pgsql()

    def save(self, **kwargs):
        old = self.getById(kwargs["id"])
        if old == None:
            sql = "insert into okooo.match(id, area, country, match_name, match_url) " \
                  "values(%(id)s, %(area)s, %(country)s, %(match_name)s, %(match_url)s);"
            self.__pgsql.insertObj(sql, **kwargs)

    def getById(self, id):
        sql = "select id, area, country, match_name, match_url from okooo.match where id=%(id)s;"
        match = self.__pgsql.getObj(sql, **{"id": id})
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
