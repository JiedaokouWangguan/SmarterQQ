import random
import time
import simplejson as json
import requests

# pgv_si = "s%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)
# print (pgv_si)
#
# pgv_pvi="%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)
# print (pgv_pvi)

print(time.time())
print("1512311739302")
print(ord("a"))

# def hash33(s):
#     e = 0
#     i = 0
#     n = len(s)
#     while n > i:
#         e += (e << 5) + ord(s[i])
#         i += 1
#     return 2147483647 & e
#
# a = '53100a6884406a09006ccf8c66f8991ebcbeb3e7a0de2bbb4b0e1595e25b1726be58aed142172c44'
#
# b = hash33(a)
# print(b)
# aa = {'result':{'vfwebqq': '7e83d9adcdcfd514d21aedbd98170af361bb0c310a83b9098618938e0146ffbaeb2c1c464ce6b9d4'},
#       'retcode':0}
# bb = json.dumps(aa)
# print(bb)

# -------------------------------第一次拿到psessionid的例子
# session = requests.Session()
# header = {
#     "Accept":"*/*",
#     "Accept-Encoding":"gzip, deflate",
#     "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
#     "Connection":"keep-alive",
#     "Content-Type":"application/x-www-form-urlencoded",
#     "Host":"d1.web2.qq.com",
#     "Origin":"http://d1.web2.qq.com",
#     "Referer":"http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2",
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
# }
# cookie = {"pgv_pvi":"9852300288",
#                 "pgv_si":"s3946728448",
#                 "RK":"Me1+Y/SvOr",
#                 "ptisp":"os",
#                 "ptcz":"be04fabfa78354a684e85975d2c6bf7154d40e4dda04408cf2af852cd5036fda",
#                 "uin":"o0592812090",
#                 "skey":"@CofPgQyGs",
#                 "pt2gguin":"o0592812090",
#                 "p_uin":"o0592812090",
#                 "pt4_token":"LqYK0yVyRP1-3QsueGQBRK81mxQhL37Yyyjcza4HyrE_",
#                 "p_skey":"-9sLzhmkzZ*CrspjmxWmBwoRFTnl7rJSbOUQ9ccKI5E_",
#                 "ptwebqq":"f7a6685523e54f8787152d75f0a2a9d3ebc5e63f9eeb656a59515ab201afc8d6"}
# session.cookies.update(cookie)
# session.headers.update(header)
# data = {"r":'{"ptwebqq":"f7a6685523e54f8787152d75f0a2a9d3ebc5e63f9eeb656a59515ab201afc8d6","clientid":53999199,"psessionid":"","status":"online"}'}
# r = session.post(url="http://d1.web2.qq.com/channel/login2", data=data)
# print(r.text)
# -------------------------------第一次拿到psessionid的例子