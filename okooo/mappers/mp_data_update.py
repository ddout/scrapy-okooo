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

    def getDotHavePlaySchList(self, page=0, limit=10):
        sql = """
                select area,country,match_name,sch_url,sch_name,sch_type,sch_group,sch_trun
                from okooo.schedule t1
                where not exists
                (
                    select 1 from okooo.play t2
                    where t1.area=t2.area
                      and t1.country=t2.country
                      and t1.match_name=t2.match_name
                      and t1.sch_name=t2.sch_name
                      and t1.sch_type=t2.sch_type
                      and t1.sch_group=t2.sch_group
                      and t1.sch_trun=t2.sch_trun
                )
                order by id asc 
                limit %(limit)s offset %(offset)s
              """
        #
        v_offset = page * limit
        v_limit = limit
        #
        params = {"offset": v_offset, "limit": v_limit}
        return self.__pgsql.getAll(sql, **params)

    def getModifyPlayList(self, page=0, limit=10):
        sql = """
                select id,area,country,match_name,sch_name,sch_type,sch_group,sch_trun,play_urls
                from okooo.play
                where 
                  (
                   (team_home is null and play_time is not null)
                    or
                       (
                       team_home is not null
                       and play_result is null
                       and play_time is not null
                       and play_time < now()
                       and play_time >= (now() - interval '10 day')
                       and play_result_detail is null
                       )
                   )
                order by paly_time desc 
                limit %(limit)s offset %(offset)s
              """
        #
        v_offset = page * limit
        v_limit = limit
        #
        params = {"offset": v_offset, "limit": v_limit}
        return self.__pgsql.getAll(sql, **params)
