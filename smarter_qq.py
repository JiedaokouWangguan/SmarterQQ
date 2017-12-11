import random
import requests
import os
import pyqrcode
import sys
import webbrowser
import time
import re
import json
from smarterqq import utils

from smarterqq import protocal


class SmarterQQ(object):

    def __init__(self):
        self.session = requests.Session()
        self.info = dict()
        self.info['qrsig'] = self.create_qrcode()
        next_url = self.check_if_login_suc()
        if next_url == "":
            sys.exit("can't login")
        self.info['ptwebqq'] = self.get_pwtwebqq(next_url)
        self.info['vfwebqq'] = self.get_vfwebqq(self.info['ptwebqq'])
        self.info['psessionid'], self.info['uin'] = self.get_permissionid_and_uin(self.info['ptwebqq'])
        self.info['clientid'] = protocal.info_clientid
        self.info['port'] = protocal.info_port
        self.info['cip'] = protocal.info_cip
        # got all the information necessary
        # ptwebqq, vfwebqq, psessionid, uin, clientid,

        # now we begin to get friends info, group info, discus info, selfinfo, online info, recent info
        self.friends_json = self.get_friends(self.info['uin'], self.info['ptwebqq'], self.info['vfwebqq'])
        self.groups_json = self.get_groups(self.info['uin'], self.info['ptwebqq'], self.info['vfwebqq'])
        self.discus_json = self.get_discus(self.info['psessionid'], self.info['vfwebqq'])
        self.selfinfo_json = self.get_selfinfo()
        self.online_json = self.get_online(self.info['vfwebqq'], self.info['psessionid'])
        self.recent_json = self.get_recent(self.info['uin'], self.info['ptwebqq'], self.info['vfwebqq'], self.info['psessionid'])
        # information is necessary since poll will probably get error message if info above is not gotten


    def create_qrcode(self):
        pwd = os.path.join(os.getcwd(), 'qrcode')
        if not os.path.exists(pwd):
            os.makedirs(pwd)
        pic_path = os.path.join(pwd, 'qrcode.png')
        url = protocal.url_get_qrcode
        result = self.session.get(url)
        with open(pic_path, 'wb') as file_output:
            file_output.write(result.content)
        # get qrsig here from cookie
        return self.session.cookies['qrsig']

    def check_if_login_suc(self):
        self.session.cookies.update(protocal.cookies_check_qrcode)
        self.session.headers.update(protocal.headers_check_qrcode)
        time_tag = 2290 + random.randrange(-9, 9)
        count = protocal.num_check_qrcode
        next_url = ""
        while count > 0:
            time_tag = time_tag + 2000 + random.randrange(-9, 9)
            url = protocal.url_check_qrcode.format(str(utils.hash33(self.info['qrsig'])), str(time_tag))
            result = self.session.get(url=url)
            reg = re.findall(r"'(.*?)'", result.text)
            code = reg[0]
            if code == protocal.code_check_qrcode_not_expires:
                print(protocal.str_check_qrcode_not_expires)
                # 未失效
            elif code == protocal.code_check_qrcode_expired:
                print(protocal.str_check_qrcode_expired)
                # 已失效
            elif code == protocal.code_check_qrcode_being_authentified:
                print(protocal.str_check_qrcode_being_authentified)
                # 认证中
            elif code == protocal.code_check_qrcode_authentified:
                print(protocal.str_check_qrcode_authentified)
                # 认证成功
                next_url = reg[2]
                break
            count -= 1
            time.sleep(protocal.time_sleep_check_qrcode)
        return next_url

    def get_pwtwebqq(self, url):
        result = self.session.get(url=url)
        return self.session.cookies['ptwebqq']

    def get_vfwebqq(self, ptwebqq):
        url = protocal.url_get_vfwebqq.format(ptwebqq, str(int(time.time()*1000)))
        headers = protocal.headers_get_vfwebqq
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j["result"]["vfwebqq"]

    def get_permissionid_and_uin(self, ptwebqq):
        payload = {'r': protocal.r_get_permissionid_and_uin.format(ptwebqq)}
        url = protocal.url_get_permissionid_and_uin
        headers = protocal.headers_get_permissionid_and_uin
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j["result"]["psessionid"], int(j["result"]["uin"])

    def get_friends(self, uin, ptwebqq, vfwebqq):
        url = protocal.url_get_friends
        headers = protocal.headers_get_friends
        hash_value = utils.hash2(uin, ptwebqq)
        payload = {'r': protocal.r_get_friends.format(vfwebqq, hash_value)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    def get_groups(self, uin, ptwebqq, vfwebqq):
        url = protocal.url_get_groups
        headers = protocal.headers_get_groups
        hash_value = utils.hash2(uin, ptwebqq)
        payload = {'r': protocal.r_get_groups.format(vfwebqq, hash_value)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    def get_discus(self, psessionid, vfwebqq):
        url = protocal.url_get_discus.format(psessionid, vfwebqq, str(int(time.time()*1000)))
        headers = protocal.headers_get_discus
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    def get_selfinfo(self):
        url = protocal.url_get_selfinfo.format(str(int(time.time()*1000)))
        headers = protocal.headers_get_selfinfo
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    def get_online(self, vfwebqq, psessionid):
        url = protocal.url_get_online.format(vfwebqq, psessionid, str(int(time.time()*1000)))
        headers = protocal.headers_get_online
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    def get_recent(self, uin, ptwebqq, vfwebqq, psessionid):
        url = protocal.url_get_recent
        headers = protocal.headers_get_recent
        hash_value = utils.hash2(uin, ptwebqq)
        payload = {'r': protocal.r_get_recent.format(vfwebqq, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    def poll(self, ptwebqq, psessionid):
        url = protocal.url_poll
        headers = protocal.headers_poll
        payload = {'r': protocal.r_get_recent.format(ptwebqq, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    def main_loop(self):
        friends_dict = dict()
        while True:
            j = self.poll(self.info['ptwebqq'], self.info['psessionid'])

            if 'result' in j.keys() and j['result'][0]['poll_type'] == 'message':
                print(j)
                text = j['result'][0]['value']['content'][1]
                from_user = str(j['result'][0]['value']['from_uin'])
                to_user = str(j['result'][0]['value']['to_uin'])
                print("from {} to {}, '{}'".format(from_user, to_user, text))
                if from_user not in friends_dict.keys():
                    url = "http://s.web2.qq.com/api/get_friend_info2?tuin=" + str(from_user) + "&vfwebqq=" + self.info[
                        "vfwebqq"] + "&clientid=53999199&psessionid=" + self.info["psessionid"] + "&t=" + str(
                        int(time.time() * 1000))
                    headers = {'Referer': 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                               'Origin': None,
                               'Host': 's.web2.qq.com',
                               'Content-Type': 'utf-8'
                               }
                    r = self.session.get(url=url, headers=headers)
                    j = r.json()
                    if 'result' in j.keys():
                        friends_dict[from_user] = {}
                        friends_dict[from_user]["info"] = j['result']  # 此处先查返回消息是否成功，如果是错误则没有'result'字段，程序崩溃
                        friends_dict[from_user]["index"] = random.randint(88000, 20000000)
                    else:
                        url = "http://d1.web2.qq.com/channel/send_buddy_msg2"
                        nick = "test"
                        send_index = str(random.randint(88000, 20000000))
                        payload = {
                            'r': '{"to":' + from_user + ',"content":"[\\"这是自动回复，你的昵称是' + nick + '\\",[\\"font\\",{\\"name\\":\\"宋体\\",\\"size\\":10,\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}]]","clientid":53999199,"msg_id":' + send_index + ',"psessionid":"' +
                                 self.info["psessionid"] + '"}'}
                        r = self.session.post(url=url, data=payload)
                        j = r.json()
                        if j["retcode"] == 0:
                            print("发送成功")
                        else:
                            print("发送失败")
                        continue

                url = "http://d1.web2.qq.com/channel/send_buddy_msg2"
                nick = friends_dict[from_user]['info']["nick"]
                send_index = str(friends_dict[from_user]["index"])
                payload = {
                    'r': '{"to":' + from_user + ',"content":"[\\"这是自动回复，你的昵称是' + nick + '\\",[\\"font\\",{\\"name\\":\\"宋体\\",\\"size\\":10,\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}]]","clientid":53999199,"msg_id":' + send_index + ',"psessionid":"' +
                         self.info["psessionid"] + '"}'}
                friends_dict[from_user]["index"] += 1
                r = self.session.post(url=url, data=payload)
                j = r.json()
                if j["retcode"] == 0:
                    print("发送成功")
                else:
                    print("发送失败")