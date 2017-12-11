import random
import time
from smarterqq import utils

# -----basic info
info_clientid = 53999199
info_port = 47450
info_cip = 23600812
# -----basic info

# ---------get qrcode---------------------
url_get_qrcode = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=' + str(
    random.random()) + '&daid=164&pt_3rd_aid=0'
# ---------get qrcode---------------------


# ---------check if qrcode expires---------------------
headers_check_qrcode = {'Referer': 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?daid=164&target=self&style=40&'
                                   'pt_disable_pwd=1&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&'
                                   's_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&'
                                   'login_state=10&t=20131024001',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                      ' AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/62.0.3202.94 Safari/537.36',
                        'Accept': '*/*',
                        'Accept-encoding': 'gzip, deflate, br',
                        'Accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
pgv_si = "s%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)
pgv_pvi="%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)
cookies_check_qrcode={'pgv_pvi':pgv_pvi,'pgv_si':pgv_si}
num_check_qrcode = 100
url_check_qrcode = "https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken={}&webqq_type=10&remember_uin=1&login2qq=1&" \
                   "aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect" \
                   "=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-{}&" \
                   "mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10232&login_sig=&pt_randsalt=0"

code_check_qrcode_not_expires = '66'
str_check_qrcode_not_expires = '二维码未失效'

code_check_qrcode_expired = '65'
str_check_qrcode_expired = '二维码已失效'

code_check_qrcode_being_authentified = '67'
str_check_qrcode_being_authentified = '二维码认证中'

code_check_qrcode_authentified = '0'
str_check_qrcode_authentified = '二维码认证成功'

time_sleep_check_qrcode = 2 # 每次请求后睡眠时间

# ---------check if qrcode expires---------------------


# -----------get vfwebqq--------------------------
url_get_vfwebqq = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq={}&clientid=53999199&psessionid=&t={}"
headers_get_vfwebqq = {'Referer':'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'}
# -----------get vfwebqq--------------------------

# ---------get permissionid and uin----------------
r_get_permissionid_and_uin = '{{"ptwebqq":"{}","clientid":53999199,"psessionid":"","status":"online"}}'
url_get_permissionid_and_uin  = "http://d1.web2.qq.com/channel/login2"
headers_get_permissionid_and_uin  = {'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
                                     'Origin':'http://d1.web2.qq.com',
                                     'Host': 'd1.web2.qq.com',
                                     'Accept-Encoding': 'gzip, deflate',
                                     'Content-Type': 'application/x-www-form-urlencoded'
}
# ---------get permissionid and uin----------------

# -----------------------get friends------------
url_get_friends = 'http://s.web2.qq.com/api/get_user_friends2'
headers_get_friends = {'Referer':'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                       'Origin':'http://s.web2.qq.com',
                       'Host': 's.web2.qq.com',
                       'Accept-Encoding': 'gzip, deflate',
                       'Content-Type': 'application/x-www-form-urlencoded'}

r_get_friends = '{{"vfwebqq":"{}","hash":"{}"}}'
# -----------------------get friends------------

# -----------------------get groups------------
url_get_groups = 'http://s.web2.qq.com/api/get_group_name_list_mask2'
headers_get_groups = {'Referer':'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                      'Origin':'http://s.web2.qq.com',
                      'Host': 's.web2.qq.com',
                      'Accept-Encoding': 'gzip, deflate',
                      'Content-Type': 'application/x-www-form-urlencoded'}

r_get_groups = '{{"vfwebqq":"{}","hash":"{}"}}'
# -----------------------get groups------------

# -----------------------get groups------------
url_get_discus = 'http://s.web2.qq.com/api/get_discus_list?clientid=53999199&psessionid={}&vfwebqq={}&t={}'
headers_get_discus = {'Referer':'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                      'Host': 's.web2.qq.com',
                      'Accept-Encoding': 'gzip, deflate',
                      'Content-Type': 'utf-8'}
# -----------------------get groups------------

# ---------------get self info-------------------
url_get_selfinfo = 'http://s.web2.qq.com/api/get_self_info2?t={}'
headers_get_selfinfo = {'Referer':'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                        'Host': 's.web2.qq.com',
                        'Accept-Encoding': 'gzip, deflate',
                        'Content-Type': 'utf-8'}
# ---------------get self info-------------------

# ----------------get online-----------------------
url_get_online = 'http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq={}&clientid=53999199&psessionid={}&t='
headers_get_online = {'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
                      'Host': 'd1.web2.qq.com',
                      'Accept-Encoding': 'gzip, deflate',
                      'Content-Type': 'utf-8'}
# ----------------get online-----------------------

# -----------------get recent----------------------
url_get_recent = 'http://d1.web2.qq.com/channel/get_recent_list2'
headers_get_recent = {'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
                      'Origin':'http://d1.web2.qq.com',
                      'Host': 'd1.web2.qq.com',
                      'Accept-Encoding': 'gzip, deflate',
                      'Content-Type': 'application/x-www-form-urlencoded'}

r_get_recent = '{{"vfwebqq":"{}","clientid":53999199,"psessionid":"{}"}}'
# -----------------get recent----------------------

# ------------------poll---------------------------
url_poll = 'http://d1.web2.qq.com/channel/poll2'
headers_poll = {'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
                    'Origin':'http://d1.web2.qq.com',
                    'Host': 'd1.web2.qq.com',
                    'Accept-Encoding': 'gzip, deflate',
                    'Content-Type': 'application/x-www-form-urlencoded'}

r_poll = '{{"ptwebqq":"{}","clientid":53999199,"psessionid":"{}","key":""}}'
# ------------------poll---------------------------



