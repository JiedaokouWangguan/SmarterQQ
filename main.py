import random
import requests
import os
import pyqrcode
import sys
import webbrowser
import time
import re
import json

def hash33(s):
    e = 0
    i = 0
    n = len(s)
    while n > i:
        e += (e << 5) + ord(s[i])
        i += 1
    return 2147483647 & e

session = requests.Session()
pwd = os.path.join(os.getcwd(), 'temp')
if not os.path.exists(pwd):
    os.makedirs(pwd)
pic_path = os.path.join(pwd, 'qrcode.png')
url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=' + str(
    random.random()) + '&daid=164&pt_3rd_aid=0'

g = session.get(url)
con = g.content
with open(pic_path, 'wb') as fout:
    fout.write(con)


headers = {'Referer':'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?daid=164&target=self&style=40&pt_disable_pwd=1&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
           'Accept':'*/*',
           'Accept-encoding':'gzip, deflate, br',
           'Accept-language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}

pgv_si = "s%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)


pgv_pvi="%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)


cookies={'pgv_pvi':pgv_pvi,
         'pgv_si':pgv_si}

session.cookies.update(cookies)

qrsig = session.cookies['qrsig']
session.headers.update(headers)
print(session.cookies.items())

# url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=http%3A%2F%2Fw.qq.com%2Fproxy.html&ptqrtoken='+str(hash33(qrsig))+'&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-'+str(int(time.time() * 1000))+'&js_ver=10232&js_type=1&login_sig=&pt_uistyle=40&aid=501004106&daid=164&mibao_css=m_webqq&'
print(url)

count = 100
next_url = ""
time_tag = 2290 + random.randrange(-9, 9)
while count > 0:
    time_tag = time_tag + 2000 + random.randrange(-9, 9)

    url = "https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=" + str(hash33(
        qrsig)) + "&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-" + str(
        time_tag) + "&mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10232&login_sig=&pt_randsalt=0"

    r = session.get(url=url)
    print(r)
    a = r.text
    print(a)
    b = re.findall(r"'(.*?)'", a)
    code = b[0]
    if code == '66':
        print("---未失效")
    elif code == '65':
        print("---已失效")
    elif code == '67':
        print("---认证中")
    elif code == '0':
        print("---认证后")
        next_url = b[2]
        print(session.cookies.items())
        break
    count -= 1
    time.sleep(2)

r = session.get(url=next_url)
print(r.content)
print("----------------------")
print(r.text)
print("----------------------")

info = {}

info['ptwebqq'] = session.cookies['ptwebqq']

url = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq="+info['ptwebqq']+"&clientid=53999199&psessionid=&t="+str(int(time.time()*1000))
headers = {'Referer':'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'}
session.headers.update(headers)
r = session.get(url)
j = r.json()
info['vfwebqq'] = j["result"]["vfwebqq"]

payload = {'r':'{"ptwebqq":"'+info["ptwebqq"]+'","clientid":53999199,"psessionid":"","status":"online"}'}
url = "http://d1.web2.qq.com/channel/login2"
headers = {'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
           'Origin':'http://d1.web2.qq.com',
           'Host': 'd1.web2.qq.com',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded'
}
session.headers.update(headers)
r = session.post(url=url,data=payload)
j = r.json()
info['psessionid'] = j["result"]["psessionid"]
info['uin'] = j["result"]["uin"]
info['clientid'] = 53999199
info['port'] = 47450
info['cip'] = 23600812

friends_dict = {}

while True:
    print(session.headers)
    payload = {'r':'{"ptwebqq":"'+info["ptwebqq"]+'","clientid":53999199,"psessionid":"'+info["psessionid"]+'","key":""}'}
    url = "http://d1.web2.qq.com/channel/poll2"
    r = session.post(url=url,data=payload)
    j = r.json()
    if 'result' in j.keys() and j['result'][0]['poll_type'] == 'message':
        print(j)
        text = j['result'][0]['value']['content'][1]
        from_user = str(j['result'][0]['value']['from_uin'])
        to_user = str(j['result'][0]['value']['to_uin'])
        print("from {} to {}, '{}'".format(from_user, to_user, text))
        if from_user not in friends_dict.keys():
            friends_dict[from_user] = {}
            url = "http://s.web2.qq.com/api/get_friend_info2?tuin="+str(from_user)+"&vfwebqq="+info["vfwebqq"]+"&clientid=53999199&psessionid="+info["psessionid"]+"&t="+str(int(time.time()*1000))
            headers = {'Referer': 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                       'Origin': None,
                       'Host': 's.web2.qq.com',
                       'Content-Type': 'utf-8'
                       }
            r = session.get(url=url, headers=headers)
            j = r.json()
            if 'result' in j.keys():
                friends_dict[from_user]["info"] = j['result'] # 此处先查返回消息是否成功，如果是错误则没有'result'字段，程序崩溃
                friends_dict[from_user]["index"] = random.randint(88000, 20000000)
            else:
                continue

        url = "http://d1.web2.qq.com/channel/send_buddy_msg2"
        nick = friends_dict[from_user]['info']["nick"]
        send_index = str(friends_dict[from_user]["index"])
        payload = {'r':'{"to":'+from_user+',"content":"[\\"这是自动回复，你的昵称是'+nick+'\\",[\\"font\\",{\\"name\\":\\"宋体\\",\\"size\\":10,\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}]]","clientid":53999199,"msg_id":'+send_index+',"psessionid":"'+info["psessionid"]+'"}'}
        friends_dict[from_user]["index"] += 1
        r = session.post(url=url,data=payload)
        j = r.json()
        if j["retcode"] == 0:
            print("发送成功")
        else:
            print("发送失败")

    else:
        time.sleep(1)