---
Author: SuperJason
Date: 2020-12-18
---

## flag
`n1book{afr_2_solved}`

## 思路
1. 访问环境时出现鬼畜舞蹈的gif，F12源码查看gif的位置在`img/img.gif`，使用目录遍历`../img`，可以看到服务器开起了文件目录索引
![](./images/afr2-1.png)
2. 思考路径穿越漏洞，访问`img../`穿越到根目录
![](./images/afr2-2.png)
3. 下载flag文件得到flag
## 总结
**文件夹与..拼接实现路径穿越**