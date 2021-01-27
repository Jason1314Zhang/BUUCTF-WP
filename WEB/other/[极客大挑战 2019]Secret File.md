---
Author: Coder-LYQ
Date: 2020-12-19
---

## flag

`flag{6a1cced5-6e86-4dd1-8cf8-5300d8c9f481}`

## 思路

1. 打开网页之后，首先观察网页上是否有信息，若无有用信息，可以F12查看源码，查找线索。

   <img src="..\images\image-20201219141626187.png" alt="image-20201219141626187" style="zoom:33%;" />

2. 源码中发现有<a></a>，其中超链接为Archive_room.php。访问该页面。

   <img src="..\images\image-20201219141826721.png" alt="image-20201219141826721" style="zoom:33%;" />

3. 点击SECRET时（访问action.php）发现，页面已显示查阅结束，且此时显示的页面为end.php，说明页面自动从action.php跳转到end.php。

   <img src="..\images\image-20201219142023904.png" alt="image-20201219142023904" style="zoom: 50%;" />

4. 类似于这种自动跳转的题目，我们可使用burpsuite进行抓包，查看中间的页面。

   <img src="..\images\image-20201219142532035.png" alt="image-20201219142532035" style="zoom:50%;" />

   拦截到action.php后，右键 Send to Repeater，在Repeater界面可以比较方便的查看Request和Response，且可以多次放松请求，和比较直观看到响应回来的数据。

   此处可以看到页面提示secr3t.php.

   <img src="..\images\image-20201219142459994.png" alt="image-20201219142459994" style="zoom:50%;" />

5. 访问secr3t.php，页面上显示一段php源码。此处开始php代码审计。

   ```php
   <?php
       highlight_file(__FILE__);
       error_reporting(0);
       $file=$_GET['file'];
       if(strstr($file,"../")||stristr($file, "tp")||stristr($file,"input")||stristr($file,"data")){
           echo "Oh no!";
           exit();
       }
       include($file); 
   //flag放在了flag.php里
   ?>
   ```

   按此段代码提示，访问secr3t.php?file=flag.php，可以看到网页显示如下。

   此处思路为F12查看源码，发现并无想要的flag，但是网页上提示“我就在这里”，说明flag可能在flag.php的源码中，因此我们应该想办法查看flag.php的源码。

   <img src="..\images\image-20201219143817671.png" alt="image-20201219143817671" style="zoom:33%;" />

   strstr(str1,str2):判断字符串str2是否是str1的子串。

   stristr(string,search,before_search): 在string中搜索search第一次出现，默认返回search之后的字符串。如果没找到，则返回False。

6. 利用**php伪协议获取源码**

   > file=php://filter/convert.base64-encode/resource=flag.php

   此时获取的内容为base64加密后的，进行一次解密即可获得flag。


## 总结

- 当页面会自动跳转到最终页面时-->利用burpsuite抓包看到中间页面
- php伪协议获取源码