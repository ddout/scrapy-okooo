# -*- coding: utf-8 -*-
# pgsql的适配器
import logging

import psycopg2
import psycopg2.extras


class Pgsql(object):
    __database = "db_ddout"
    __dbuser = "ddout"
    __password = "ddout"
    __host = "192.168.56.101"
    __port = "5432"

    __connect = None
    __cursor = None

    def __init__(self):
        self.__connect = psycopg2.connect(database=self.__database, user=self.__dbuser, password=self.__password,
                                          host=self.__host, port=self.__port)
        logging.debug("Opened database successfully")
        self.__cursor = self.__connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        logging.debug("Opened database.cursor successfully")

    def execSql(self, sql):
        try:
            self.__cursor.execute(sql)
            self.__connect.commit()
        except:
            self.__connect.rollback()

        return None

    def insertObj(self, sql, **kwargs):
        try:
            logging.debug("sql:", sql, "kwargs:", kwargs)
            print("sql:", sql, "kwargs:", kwargs)
            self.__cursor.execute(sql, kwargs)
            self.__connect.commit()
            logging.debug("insert into Success!")
        except Exception, e:
            self.__connect.rollback()
            logging.error(msg=e)
        return None

    def getObj(self, sql, **kwargs):
        try:
            logging.debug("sql:", sql, "kwargs:", kwargs)
            print("sql:", sql, "kwargs:", kwargs)
            self.__cursor.execute(sql, kwargs)
            obj = self.__cursor.fetchone()
            logging.debug("getObj Success!")
            return obj
        except Exception, e:
            self.__connect.rollback()
            logging.error(msg=e)
        return None

    def getAll(self, sql, **kwargs):
        try:
            logging.debug("sql:", sql, "kwargs:", kwargs)
            print("sql:", sql, "kwargs:", kwargs)
            self.__cursor.execute(sql, kwargs)
            obj = self.__cursor.fetchall()
            logging.debug("getObj Success!")
            return obj
        except Exception, e:
            self.__connect.rollback()
            logging.error(msg=e)
        return None
