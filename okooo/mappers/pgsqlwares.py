# -*- coding: utf-8 -*-
# pgsql的适配器
import logging

import psycopg2
import psycopg2.extras
import psycopg2.pool

from okooo.app_configure import app_config


class Pgsql(object):
    __database = app_config["pgsql"]["database"]
    __dbuser = app_config["pgsql"]["dbuser"]
    __password = app_config["pgsql"]["password"]
    __host = app_config["pgsql"]["host"]
    __port = app_config["pgsql"]["port"]
    __minconn = app_config["pgsql"]["minconn"]
    __maxconn = app_config["pgsql"]["maxconn"]
    #
    __dbpool = None

    #

    def __init__(self):
        self.__dbpool = psycopg2.pool.ThreadedConnectionPool(self.__minconn, self.__maxconn, database=self.__database,
                                                             user=self.__dbuser,
                                                             password=self.__password,
                                                             host=self.__host, port=self.__port)
        logging.debug("Opened database Pool successfully")

    def getConn(self):
        return self.__dbpool.getconn()

    def getCursor(self, conn):
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def closeConn(self, conn):
        if conn != None:
            self.__dbpool.putconn(conn)

    def execSql(self, sql, **kwargs):
        conn = self.getConn()
        try:
            print("insertObj", " sql:", sql, " kwargs:", kwargs)
            cursor = self.getCursor(conn)
            cursor.execute(sql, kwargs)
            conn.commit()
        except:
            conn.rollback()
        finally:
            self.closeConn(conn)
        return None

    def insertObj(self, sql, **kwargs):
        conn = self.getConn()
        try:
            print("insertObj", " sql:", sql, " kwargs:", kwargs)
            cursor = self.getCursor(conn)
            cursor.execute(sql, kwargs)
            conn.commit()
        except Exception, e:
            logging.error(msg=e)
            conn.rollback()
        finally:
            self.closeConn(conn)
        return None

    def modifyObj(self, sql, **kwargs):
        conn = self.getConn()
        try:
            print("modifyObj", " sql:", sql, " kwargs:", kwargs)
            cursor = self.getCursor(conn)
            cursor.execute(sql, kwargs)
            conn.commit()
        except Exception, e:
            logging.error(msg=e)
            conn.rollback()
        finally:
            self.closeConn(conn)
        return None

    def getObj(self, sql, **kwargs):
        conn = self.getConn()
        try:
            print("getObj", " sql:", sql, " kwargs:", kwargs)
            cursor = self.getCursor(conn)
            cursor.execute(sql, kwargs)
            obj = cursor.fetchone()
            return obj
        except Exception, e:
            logging.error(msg=e)
            conn.rollback()
        finally:
            self.closeConn(conn)
        return None

    def getAll(self, sql, **kwargs):
        conn = self.getConn()
        try:
            print("getAll", " sql:", sql, " kwargs:", kwargs)
            cursor = self.getCursor(conn)
            cursor.execute(sql, kwargs)
            rows = cursor.fetchall()
            return rows
        except Exception, e:
            conn.rollback()
            logging.error(msg=e)
        finally:
            self.closeConn(conn)
        return None
