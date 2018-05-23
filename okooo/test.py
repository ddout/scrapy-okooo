# -*- coding: utf-8 -*-
import json
import time

import psycopg2
import psycopg2.pool
import psycopg2.extras

__database = "db_ddout"
__dbuser = "ddout"
__password = "ddout"
__host = "192.168.56.101"
__port = "5432"
#
dbpool = psycopg2.pool.SimpleConnectionPool(1, 10, dbname=__database, user=__dbuser, host=__host, password=__password,
                                            port=__port)
conn = dbpool.getconn()
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
try:
    sql1 = """
    insert into okooo.test(id,name,bri,tjson)
    values(%s,%s,%s,%s);
    """
    cursor.execute(sql1, (1, None, "2013-04-03 18:00".replace(" "," "),
                          '{"name":"a","age":"12","child":{"name":"a","age":"12"}, "childen":[{"name":"a","age":"12"},{"name":"a","age":"12"}]}'))
    conn.commit()
    #
    sqlstr = "select * from okooo.test"
    cursor.execute(sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        print(row["bri"])
except Exception, e:
    print(e)
finally:
    dbpool.putconn(conn)

dbpool.closeall()
