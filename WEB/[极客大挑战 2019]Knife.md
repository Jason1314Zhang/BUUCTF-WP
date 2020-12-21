---
Author: Coder-LYQ
Date: 2020-12-19
---

## flag
flag{07a49b96-3638-45f3-aed5-b08cd8e30467}

## 思路

1. 打开网页，可以看到网页显示如下：

    <img src=".\images\image-20201221.png" alt="image-20201219141626187" style="zoom:33%;" />
    
    题目提示的比较明显，有菜刀，而且有常见的一句话木马`eval($_POST["Syc"])`
    因此顺其自然的利用菜刀/御剑进行连接。