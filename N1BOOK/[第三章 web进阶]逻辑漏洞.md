---
Author: SuperJason
Date: 2020-12-28
---

## flag
`FLAG{you_can_got_it}`

## 思路
1. 打开题目环境，任意输入用户名、密码，得到以下界面  

<img src="images/image-20201228195652567.png" alt="image-20201228195652567" style="zoom: 50%;" />



2. 无法直接购买flag书籍，显示钱不够，通过burpsuite抓包分析购买操作。发现cost参数和goods参数。利用逻辑漏洞给书籍价格添加负值价格，增加money，然后可以购买flag。  

   ![image-20201228200458017](images/image-20201228200458017.png)
