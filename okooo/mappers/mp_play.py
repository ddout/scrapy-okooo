# -*- coding: utf-8 -*-
from pgsqlwares import Pgsql


class PlayMapper(object):
    __pgsql = None

    def __init__(self):
        self.__pgsql = Pgsql()

    def save(self, **kwargs):
        old = self.getById(kwargs["id"])
        if old == None:
            sql = "insert into okooo.play(id, play_urls, area, country, match_name, " \
                  " sch_name, sch_type, sch_group, sch_trun, play_time, team_home, " \
                  " team_vis, half_home, half_vis, full_home, full_vis,play_result, odds_info) " \
                  " values(%(id)s, %(play_urls)s, %(area)s, %(country)s, %(match_name)s, " \
                  " %(sch_name)s, %(sch_type)s, %(sch_group)s, %(sch_trun)s, %(play_time)s, " \
                  " %(team_home)s, %(team_vis)s, %(half_home)s, %(half_vis)s, %(full_home)s, " \
                  " %(full_vis)s, %(play_result)s, %(odds_info)s );"
            self.__pgsql.insertObj(sql, **kwargs)
        else:
            sql = "update okooo.play set " \
                  " play_urls=%(play_urls)s, area=%(area)s, country=%(country)s, " \
                  " match_name=%(match_name)s, sch_name=%(sch_name)s, " \
                  " sch_type=%(sch_type)s, sch_group=%(sch_group)s, " \
                  " sch_trun=%(sch_trun)s, play_time=%(play_time)s, " \
                  " team_home=%(team_home)s, team_vis=%(team_vis)s, " \
                  " half_home=%(half_home)s, half_vis=%(half_vis)s, " \
                  " full_home=%(full_home)s, full_vis=%(full_vis)s, " \
                  " play_result=%(play_result)s, odds_info=%(odds_info)s " \
                  " where id=%(id)s"
            self.__pgsql.modifyObj(sql, **kwargs)

    def getById(self, id):
        sql = "select id from okooo.play where id=%(id)s;"
        obj = self.__pgsql.getObj(sql, **{"id": id})
        return obj

    def getSchList(self, page=0, limit=10):
        sql = "select area,country,match_name,sch_url,sch_name,sch_type,sch_group,sch_trun from okooo.schedule " \
              " order by sch_url asc " \
              " limit %(limit)s offset %(offset)s ;"
        #
        v_offset = page * limit
        v_limit = limit
        #
        params = {"offset": v_offset, "limit": v_limit}
        return self.__pgsql.getAll(sql, **params)

