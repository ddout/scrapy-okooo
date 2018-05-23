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
# dbpool = psycopg2.pool.SimpleConnectionPool(1, 10, dbname=__database, user=__dbuser, host=__host, password=__password,
#                                             port=__port)
# conn = dbpool.getconn()
# cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
# try:
#     sql1 = """
#     insert into okooo.test(id,name,bri,tjson)
#     values(%s,%s,%s,%s);
#     """
#     cursor.execute(sql1, (1, None, "01-01-20 23:33:21",
#                           '{"name":"a","age":"12","child":{"name":"a","age":"12"}, "childen":[{"name":"a","age":"12"},{"name":"a","age":"12"}]}'))
#     conn.commit()
#     #
#     sqlstr = "select * from okooo.test"
#     cursor.execute(sqlstr)
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row["name"])
# except Exception, e:
#     print(e)
# finally:
#     dbpool.putconn(conn)
#
# dbpool.closeall()

#
# print("半:1-1".strip().replace("半:","").split("-"))
# str = "69-04-08 21:15"
# t = "2017-11-24 17:30:00"
# # 将其转换为时间数组
# timeStruct = time.strptime(str, "%y-%m-%d %H:%M")
# # 转换为时间戳:
# timeStamp = int(time.mktime(timeStruct))
# print(timeStamp)
# # timeStamp = 1511515800
# localTime = time.localtime(timeStamp)
# strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
# print(strTime)
#
# print("/soccer/match/954629/odds/ajax/?page=0&trnum={0}&companytype=AuthoriteBooks&type=1".format("5"))


str = """
<script>
    var data_str = '[]';
    var static_str = '{"count":5,"max":{"Start":{"home":"6.00","draw":"3.75","away":"1.75"},"End":{"home":"5.50","draw":"3.50","away":"1.75"},"Radio":{"home":"20.51","draw":"27.63","away":"55.28"},"Kelly":{"home":"1.00","draw":"0.93","away":"0.97"},"Payoff":"0.95","Boundary":null,"StartBoundary":null},"min":{"Start":{"home":"4.40","draw":"3.39","away":"1.62"},"End":{"home":"4.40","draw":"3.40","away":"1.68"},"Radio":{"home":"17.09","draw":"25.78","away":"53.71"},"Kelly":{"home":"0.80","draw":"0.90","away":"0.93"},"Payoff":"0.90","Boundary":null,"StartBoundary":null},"avg":{"Start":{"home":"5.26","draw":"3.51","away":"1.68"},"End":{"home":"5.07","draw":"3.44","away":"1.72"},"Radio":{"home":"18.50","draw":"27.15","away":"54.35"},"Kelly":{"home":"0.92","draw":"0.91","away":"0.95"},"Payoff":"0.93","Boundary":0,"StartBoundary":0},"variance":{"KD":{"home":"6.75","draw":"1.30","away":"1.37"},"KV":{"home":"46","draw":"2","away":"2"},"OE":{"home":"0.71","draw":"0.89","away":"0.93"}}}';    var pageData = eval("(" + data_str + ")");
    var checkAjaxDataOver = 1;
    var needLogin = '0';
    </script>
"""
print(len("var data_str = '"))
print(str.index("var data_str = '"))
print(str[str.index("var data_str = '") + 15: str.index("var static_str =")].strip()[1:-2])
