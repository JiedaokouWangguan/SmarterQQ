#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main module """

__author__ = 'JiedaokouWangguan'

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
from smarterqq import protocol


class SmarterQQ(object):

    def __init__(self, stra_obj):
        self.stra_obj = stra_obj
        self.session = requests.Session()
        self.info = dict()
        self.info['qrsig'] = self.create_qrcode()
        next_url = self.check_if_login_suc()
        if next_url == "":
            sys.exit("can't login")
        self.info['ptwebqq'] = self.get_pwtwebqq(next_url)
        self.info['vfwebqq'] = self.get_vfwebqq(self.info['ptwebqq'])
        self.info['psessionid'], self.info['uin'] = self.get_permissionid_and_uin(self.info['ptwebqq'])
        self.info['clientid'] = protocol.info_clientid
        self.info['port'] = protocol.info_port
        self.info['cip'] = protocol.info_cip
        # got all the information necessary
        # ptwebqq, vfwebqq, psessionid, uin, clientid,

        # now we begin to get friends info, group info, discus info, selfinfo, online info, recent info
        self.friends_json = self.get_friends(self.info['uin'], self.info['ptwebqq'], self.info['vfwebqq'])
        self.groups_json = self.get_groups(self.info['uin'], self.info['ptwebqq'], self.info['vfwebqq'])
        self.discus_json = self.get_discus(self.info['psessionid'], self.info['vfwebqq'])
        self.selfinfo_json = self.get_selfinfo()
        self.online_json = self.get_online(self.info['vfwebqq'], self.info['psessionid'])
        self.recent_json = self.get_recent(self.info['uin'], self.info['ptwebqq'], self.info['vfwebqq'],
                                           self.info['psessionid'])
        # information is necessary since poll will probably get error message if info above is not gotten

        # init strategy object
        self.stra_obj.set_info(self.friends_json, self.groups_json, self.discus_json, self.online_json,
                               self.recent_json, self.selfinfo_json)

    def create_qrcode(self):
        pwd = os.path.join(os.getcwd(), 'qrcode')
        if not os.path.exists(pwd):
            os.makedirs(pwd)
        pic_path = os.path.join(pwd, 'qrcode.png')
        url = protocol.url_get_qrcode
        result = self.session.get(url)
        with open(pic_path, 'wb') as file_output:
            file_output.write(result.content)
        # get qrsig here from cookie
        return self.session.cookies['qrsig']

    def check_if_login_suc(self):
        self.session.cookies.update(protocol.cookies_check_qrcode)
        self.session.headers.update(protocol.headers_check_qrcode)
        time_tag = 2290 + random.randrange(-9, 9)
        count = protocol.num_check_qrcode
        next_url = ""
        while count > 0:
            time_tag = time_tag + 2000 + random.randrange(-9, 9)
            url = protocol.url_check_qrcode.format(str(utils.hash33(self.info['qrsig'])), str(time_tag))
            result = self.session.get(url=url)
            reg = re.findall(r"'(.*?)'", result.text)
            code = reg[0]
            if code == protocol.code_check_qrcode_not_expires:
                print(protocol.str_check_qrcode_not_expires)
                # 未失效
            elif code == protocol.code_check_qrcode_expired:
                print(protocol.str_check_qrcode_expired)
                # 已失效
            elif code == protocol.code_check_qrcode_being_authentified:
                print(protocol.str_check_qrcode_being_authentified)
                # 认证中
            elif code == protocol.code_check_qrcode_authentified:
                print(protocol.str_check_qrcode_authentified)
                # 认证成功
                next_url = reg[2]
                break
            count -= 1
            time.sleep(protocol.time_sleep_check_qrcode)
        return next_url

    def get_pwtwebqq(self, url):
        result = self.session.get(url=url)
        return self.session.cookies['ptwebqq']

    def get_vfwebqq(self, ptwebqq):
        url = protocol.url_get_vfwebqq.format(ptwebqq, str(int(time.time() * 1000)))
        headers = protocol.headers_get_vfwebqq
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j["result"]["vfwebqq"]

    def get_permissionid_and_uin(self, ptwebqq):
        payload = {'r': protocol.r_get_permissionid_and_uin.format(ptwebqq)}
        url = protocol.url_get_permissionid_and_uin
        headers = protocol.headers_get_permissionid_and_uin
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j["result"]["psessionid"], int(j["result"]["uin"])

    def get_friends(self, uin, ptwebqq, vfwebqq):
        url = protocol.url_get_friends
        headers = protocol.headers_get_friends
        hash_value = utils.hash2(uin, ptwebqq)
        payload = {'r': protocol.r_get_friends.format(vfwebqq, hash_value)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    def get_groups(self, uin, ptwebqq, vfwebqq):
        url = protocol.url_get_groups
        headers = protocol.headers_get_groups
        hash_value = utils.hash2(uin, ptwebqq)
        payload = {'r': protocol.r_get_groups.format(vfwebqq, hash_value)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    def get_discus(self, psessionid, vfwebqq):
        url = protocol.url_get_discus.format(psessionid, vfwebqq, str(int(time.time() * 1000)))
        headers = protocol.headers_get_discus
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    def get_selfinfo(self):
        url = protocol.url_get_selfinfo.format(str(int(time.time() * 1000)))
        headers = protocol.headers_get_selfinfo
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    def get_online(self, vfwebqq, psessionid):
        url = protocol.url_get_online.format(vfwebqq, psessionid, str(int(time.time() * 1000)))
        headers = protocol.headers_get_online
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    def get_recent(self, uin, ptwebqq, vfwebqq, psessionid):
        url = protocol.url_get_recent
        headers = protocol.headers_get_recent
        hash_value = utils.hash2(uin, ptwebqq)
        payload = {'r': protocol.r_get_recent.format(vfwebqq, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    # receive message
    def poll(self, ptwebqq, psessionid):
        url = protocol.url_poll
        headers = protocol.headers_poll
        payload = {'r': protocol.r_get_recent.format(ptwebqq, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    # get friend info
    def get_friendinfo(self, friend_uin, vfwebqq, psessionid):
        url = protocol.url_get_friendinfo.format(str(friend_uin), vfwebqq, psessionid, str(int(time.time() * 1000)))
        headers = protocol.headers_get_friendinfo
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    # send message
    def send_msg(self, fromuser_uin, msg_content, msg_index, psessionid):
        url = protocol.url_send_msg
        headers = protocol.headers_send_msg
        payload = {'r': protocol.r_send_msg.format(fromuser_uin, msg_content, msg_index, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j['retcode']

    def main_loop(self):
        print("in main loop...")
        users_info = dict()
        while True:
            print("polling...")
            j = self.poll(self.info['ptwebqq'], self.info['psessionid'])
            if 'result' in j.keys() and j['result'][0]['poll_type'] == 'message':
                # msg from another user
                from_user = str(j['result'][0]['value']['from_uin'])

                if from_user not in users_info.keys():
                    j = self.get_friendinfo(from_user, self.info['vfwebqq'], self.info['psessionid'])
                    if 'result' in j.keys():
                        users_info[from_user] = {}
                        users_info[from_user]["info"] = j['result']
                        users_info[from_user]["index"] = random.randint(88000, 20000000)
                    else:
                        continue
                # set msg index for each user

                replay_content = self.stra_obj.get_msg_reply(j, users_info[from_user]['info'])
                msg_index = users_info[from_user]['index']
                return_code = self.send_msg(from_user, replay_content, msg_index, self.info['psessionid'])
                if return_code == protocol.code_send_msg_suc:
                    users_info[from_user]['index'] += 1
                    print(protocol.str_send_msg_suc)
                else:
                    print(protocol.str_send_msg_failed)

            # elif group msg

            # elif discus msg

