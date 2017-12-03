import random
import requests
import os
import pyqrcode
import sys
import webbrowser
import time
import re

UNKONWN = 'unkonwn'
SUCCESS = '200'
SCANED = '201'
TIMEOUT = '408'

class SafeSession(requests.Session):
    def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None,
                json=None):
        for i in range(3):
            try:
                return super(SafeSession, self).request(method, url, params, data, headers, cookies, files, auth,
                                                        timeout,
                                                        allow_redirects, proxies, hooks, stream, verify, cert, json)
            except Exception as e:
                print(e.message)
                continue

        #重试3次以后再加一次，抛出异常
        try:
            return super(SafeSession, self).request(method, url, params, data, headers, cookies, files, auth,
                                                    timeout,
                                                    allow_redirects, proxies, hooks, stream, verify, cert, json)
        except Exception as e:
            raise e

class test(object):

    def __init__(self):
        self.session = SafeSession()
        self.session.headers.update({'Referer':'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?daid=164&target=self&style=40&pt_disable_pwd=1&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001',
                                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})

    def do_request(self, url):
        r = self.session.get(url)
        r.encoding = 'utf-8'
        print(r)
        return r

    def wait4login(self):
        """
        http comet:
        tip=1, 等待用户扫描二维码,
               201: scaned
               408: timeout
        tip=0, 等待用户确认登录,
               200: confirmed
        """
        # temple = 'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=http%3A%2F%2Fw.qq.com%2Fproxy.html&ptqrtoken=1071800943&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-{}&js_ver=10232&js_type=1&login_sig=&pt_uistyle=40&aid=501004106&daid=164&mibao_css=m_webqq&'
        temple = 'https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&remember_uin=1&login2qq=1&aid=501004106 &u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10 &ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert &action=0-0-157510&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10143&login_sig=&pt_randsalt=0'

        tip = 1

        try_later_secs = 1
        MAX_RETRY_TIMES = 20

        code = UNKONWN

        retry_time = MAX_RETRY_TIMES
        while retry_time > 0:
            #  url = temple.format(int(time.time()*1000))
            r = self.do_request(temple)

            # if code == SCANED:
            #     print('[INFO] Please confirm to login .')
            #     tip = 0
            # elif code == SUCCESS:  # 确认登录成功
            #     param = re.search(r'window.redirect_uri="(\S+?)";', data)
            #     redirect_uri = param.group(1) + '&fun=new'
            #     self.redirect_uri = redirect_uri
            #     self.base_uri = redirect_uri[:redirect_uri.rfind('/')]
            #     temp_host = self.base_uri[8:]
            #     self.base_host = temp_host[:temp_host.find("/")]
            #     return code
            # elif code == TIMEOUT:
            #     print
            #     '[ERROR] WeChat login timeout. retry in %s secs later...' % (try_later_secs,)
            #
            #     tip = 1  # 重置
            #     retry_time -= 1
            #     time.sleep(try_later_secs)
            # else:
            #     print('[ERROR] WeChat login exception return_code=%s. retry in %s secs later...' %
            #           (code, try_later_secs))
            #     tip = 1
            retry_time -= 1
            time.sleep(try_later_secs)

        return code

    def show_image(self, file_path):
        """
        跨平台显示图片文件
        :param file_path: 图片文件路径
        """
        if sys.version_info >= (3, 3):
            from shlex import quote
        else:
            from pipes import quote

        if sys.platform == "darwin":
            command = "open -a /Applications/Preview.app %s&" % quote(file_path)
            os.system(command)
        else:
            webbrowser.open(os.path.join(os.getcwd(), 'temp', file_path))

    def main_method(self):
        pwd = os.path.join(os.getcwd(), 'temp')
        if os.path.exists(pwd) == False:
            os.makedirs(pwd)
        pic_path = os.path.join(pwd, 'test1.png')
        url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=' + str(
            random.random()) + '&daid=164&pt_3rd_aid=0'
        qr = pyqrcode.create(url)
        self.session.get(url)

        qr.png(pic_path, scale=8)
        self.show_image(pic_path)
        self.wait4login()

def show_image(file_path):
    """
    跨平台显示图片文件
    :param file_path: 图片文件路径
    """
    if sys.version_info >= (3, 3):
        from shlex import quote
    else:
        from pipes import quote

    if sys.platform == "darwin":
        command = "open -a /Applications/Preview.app %s&" % quote(file_path)
        os.system(command)
    else:
        webbrowser.open(os.path.join(os.getcwd(), 'temp', file_path))

session = requests.Session()
pwd = os.path.join(os.getcwd(), 'temp')
if os.path.exists(pwd) == False:
    os.makedirs(pwd)
# pic_path = os.path.join(pwd, 'test1.png')
# url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=' + str(
#     random.random()) + '&daid=164&pt_3rd_aid=0'
# qr = pyqrcode.create(url)
# qr.png(pic_path, scale=8)
# show_image(pic_path)
# r = session.get(url)
headers = {'Referer':'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?daid=164&target=self&style=40&pt_disable_pwd=1&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
           'Accept':'*/*',
           'Accept-encoding':'gzip, deflate, br',
           'Accept-language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}

cookies={'pgv_pvi':'4254048256',
         'pgv_si':'s9238019072',
         'qrsig':'AzVLSlAvnty-nwG8iAYuf6dHTBLny9TuHRGj9LrvE1*pMMMfosnPi8ksjCcPET0J'}

url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=http%3A%2F%2Fw.qq.com%2Fproxy.html&ptqrtoken=574853233&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1511828901879&js_ver=10232&js_type=1&login_sig=&pt_uistyle=40&aid=501004106&daid=164&mibao_css=m_webqq&'
r = session.get(url=url,headers=headers,cookies=cookies)
a = r.text
b = re.findall(r"'(.*?)'", a)
for bb in b:
    print(bb)
tmp = random.random()
