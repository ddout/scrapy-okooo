# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.pool

__database = "db_ddout"
__dbuser = "ddout"
__password = "ddout"
__host = "192.168.56.101"
__port = "5432"

dbpool = psycopg2.pool.SimpleConnectionPool(1, 10, dbname=__database, user=__dbuser, host=__host, password=__password,
                                              port=__port)
conn = dbpool.getconn()
cursor = conn.cursor()
sqlstr = "select count(1) from okooo.match"
cursor.execute(sqlstr)
rows = cursor.fetchall()
for row in rows:
    print "name", row[0]
dbpool.putconn(conn)
