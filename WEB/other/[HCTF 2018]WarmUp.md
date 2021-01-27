---
Author: SuperJason
Date: 2020-12-30
---

## flag
`flag{2d746d85-0a38-4c88-b641-435fddb48cf2}`

## 思路
1. 访问环境。f12注释中提示`source.php`，代码审计，设置了白名单source.php和hint.php，只有checkFile函数为true时，才会包含文件。并且checkFile函数最后一个`return true`判断的是截取后的字符串，存在利用点。  
2. hint.php内容`flag not here, and flag in ffffllllaaaagggg`，提示flag在`ffffllllaaaagggg`处
3. 构造`source.php?file=source.php?../../../../../../../ffffllllaaaagggg`获得flag，第二个source.php后面加?是为了绕过白名单，`source.php?../../../../../../../ffffllllaaaagggg`被include。
4. 源代码
```php
<?php
    highlight_file(__FILE__);
    class emmm
    {
        public static function checkFile(&$page)
        {
            $whitelist = ["source"=>"source.php","hint"=>"hint.php"];
            if (! isset($page) || !is_string($page)) {
                echo "you can't see it";
                return false;
            }

            if (in_array($page, $whitelist)) {
                return true;
            }

            $_page = mb_substr(
                $page,
                0,
                mb_strpos($page . '?', '?')
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }

            $_page = urldecode($page);
            $_page = mb_substr(
                $_page,
                0,
                mb_strpos($_page . '?', '?')
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }
            echo "you can't see it";
            return false;
        }
    }

    if (! empty($_REQUEST['file'])
        && is_string($_REQUEST['file'])
        && emmm::checkFile($_REQUEST['file'])
    ) {
        include $_REQUEST['file'];
        exit;
    } else {
        echo "<br><img src=\"https://i.loli.net/2018/11/01/5bdb0d93dc794.jpg\" />";
    }  
?>
```