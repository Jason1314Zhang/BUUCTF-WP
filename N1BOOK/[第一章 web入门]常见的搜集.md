---
Author: SuperJason
Date: 2020-12-18
---

## flag
`n1book{info_1s_v3ry_imp0rtant_hack}`

## 思路
1. 在本机上使用docker构建环境时，可以用[dirsearch](https://github.com/maurosoria/dirsearch)扫描服务器文件，可以得到以下文件
- robots.txt  `flag1:n1book{info_1`
- index.php~  `flag2:s_v3ry_im`
- .index.php.swp  `flag3:p0rtant_hack}`

2. 在BUUCTF平台上，对同一个IP的访问进行了限制，此时使用dirsearch无效，需要通过经验访问`robots.txt`、`index.php~`、`.index.php.swp`、`index.php.bak`
3. `.index.php.swp`是在vim编辑器异常退出时保留的备份文件，可以用**vim -r .index.php.swp**（建议使用WSL，不用开启Linux虚拟机）恢复原始内容

