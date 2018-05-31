# -*- coding: utf-8 -*-


import base64, urllib, urllib2
import json

from okooo.app_configure import app_config


def getImgBase64(path):
    with open(path, "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
        # base64.b64decode(base64data)
    return base64_data


def getYZM(img_base64):
    host = 'http://txyzmsb.market.alicloudapi.com'
    path = '/yzm'
    method = 'POST'
    appcode = app_config["yzm_cfg"]["appcode"]
    querys = ''
    bodys = {}
    url = host + path

    bodys['v_pic'] = img_base64
    bodys['v_type'] = '''ne5'''
    post_data = urllib.urlencode(bodys)
    request = urllib2.Request(url, post_data)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    # 根据API的要求，定义相对应的Content - Type
    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        data = json.loads(content)
        if data.get("errCode") == 0:
            return data.get("v_code")
