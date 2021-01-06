---
Author: Coder-LYQ
Date: 2021-1-5
---

## 思路

1. 打开网页，显示可以注册和登录。

   注册是一个写入数据库的过程，登录是查询数据库的过程，所以可以大致推测本题可能存在二次注入。

<img src="images/image-20210106212214557.png" alt="image-20210106212214557" style="zoom:50%;" />

2. 首先测试注册过程是否存在waf，输入如下，会弹出invalid string。

   <img src="images/image-20210106212522917.png" alt="image-20210106212522917" style="zoom:50%;" />

3. 

## 总结

   - 本题的核心是SQL二次注入，是学习SQL二次注入的比较好的例子。
   - 报错型注入
   - 当flag很长时需要两次获取，reverse函数的使用