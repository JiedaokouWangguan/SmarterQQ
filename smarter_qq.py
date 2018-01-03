#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main module """

__author__ = 'JiedaokouWangguan'

import random
import requests
import os
import sys
import time
import re
from smarterqq import utils
from smarterqq import protocol
import pickle


class SmarterQQ(object):
    def __init__(self, stra_obj):
        self.stra_obj = stra_obj
        self.session = requests.Session()
        # try loading info and cookie

        if not self.login_with_cookies():
            self.info = dict()
            self.info['qrsig'] = self.create_qrcode()
            next_url = self.check_if_login_suc()
            if next_url == "":
                sys.exit("can't login")
            self.info['ptwebqq'] = self.get_pwtwebqq(next_url)
            # save info and cookie
            self.save_info_cookies()
            vfwebqq_result = self.get_vfwebqq(self.info['ptwebqq'])
            self.info['vfwebqq'] = vfwebqq_result["result"]["vfwebqq"]
            print(protocol.str_login_with_qrcode)

        print(protocol.str_loading_info)
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
        self.recent_json = self.get_recent(self.info['vfwebqq'], self.info['psessionid'])
        # information is necessary since poll will probably get error message if info above is not gotten

        self.friends_info_detail = {}
        self.group_info_detail = {}
        self.discus_info_detail = {}

        # init strategy object
        self.stra_obj.set_info(self.friends_json, self.groups_json, self.discus_json, self.online_json,
                               self.recent_json, self.selfinfo_json)

    def login_with_cookies(self):
        if not self.load_info_cookies():
            return False
        vfwebqq_result = self.get_vfwebqq(self.info['ptwebqq'])
        if vfwebqq_result['retcode'] != 0:
            print(protocol.str_login_failed_to_get_vfwebqq)
            return False
        self.info['vfwebqq'] = vfwebqq_result["result"]["vfwebqq"]
        print(protocol.str_login_with_cookies)
        return True

    def load_info_cookies(self):
        pwd = os.path.join(os.getcwd(), 'save')
        cookies_path = os.path.join(pwd, 'cookies.sy')
        info_path = os.path.join(pwd, 'info.sy')
        if not (os.path.exists(pwd) and os.path.exists(cookies_path) and os.path.exists(info_path)):
            print(protocol.str_login_files_missing)
            return False

        with open(cookies_path, 'rb') as cookies_file:
            cookies = pickle.load(cookies_file)
        with open(info_path, 'rb') as info_file:
            info = pickle.load(info_file)
        self.info = info
        self.session.cookies = cookies
        return True

    def save_info_cookies(self):
        pwd = os.path.join(os.getcwd(), 'save')
        if not os.path.exists(pwd):
            os.makedirs(pwd)
        cookies_path = os.path.join(pwd, 'cookies.sy')
        info_path = os.path.join(pwd, 'info.sy')
        with open(cookies_path, 'wb') as cookies_file:
            pickle.dump(self.session.cookies, cookies_file)
        with open(info_path, 'wb') as info_file:
            pickle.dump(self.info, info_file)

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
        self.session.get(url=url)
        return self.session.cookies['ptwebqq']

    def get_vfwebqq(self, ptwebqq):
        url = protocol.url_get_vfwebqq.format(ptwebqq, str(int(time.time() * 1000)))
        headers = protocol.headers_get_vfwebqq
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    def get_permissionid_and_uin(self, ptwebqq):
        payload = {'r': protocol.r_get_permissionid_and_uin.format(ptwebqq)}
        url = protocol.url_get_permissionid_and_uin
        headers = protocol.headers_get_permissionid_and_uin
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j["result"]["psessionid"], int(j["result"]["uin"])

    # get_friends
    """
    {
        "retcode":0,
        "result":
            {
            "friends":
                [
                    ...
                    {flag: 48, uin: 336292125, categories: 12},
                    ...
                ],
            "info":
                [
                    ...
                    {face: 348, flag: {flag}, nick: "{nick}", uin: {uin}},
                    ...
                ],
            "categories":
                [
                    ...
                    {index: 0, sort: 1, name: "{name}"},
                    ...
                ],
            "marknames":
                [
                    ... 
                    {uin: {uin}, markname: "{markname}", type: 0},
                    ...
                ],
            "vipinfo":
                [
                    ...
                    {vip_level: {vip_level}, u: {u}, is_vip: 0},
                    ...
                ]
            }
    }
    """

    def get_friends(self, uin, ptwebqq, vfwebqq):
        url = protocol.url_get_friends
        headers = protocol.headers_get_friends
        hash_value = utils.hash2(uin, ptwebqq)
        payload = {'r': protocol.r_get_friends.format(vfwebqq, hash_value)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        if j["retcode"] == 0:
            print(protocol.str_get_friends_suc)
            return j['result']
        else:
            print(protocol.str_get_friends_failed)

    # get_groups
    """
    {
        "result":
            {
                "gmarklist":[],
                "gmasklist":[],
                "gnamelist":
                    [
                        ...
                        {flag:{flag}, name: "{name}", gid: {gid}, code: {code}},
                        ...
                    ]
            retcode:0
    }
    """

    def get_groups(self, uin, ptwebqq, vfwebqq):
        url = protocol.url_get_groups
        headers = protocol.headers_get_groups
        hash_value = utils.hash2(uin, ptwebqq)
        payload = {'r': protocol.r_get_groups.format(vfwebqq, hash_value)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        if j["retcode"] == 0:
            print(protocol.str_get_group_suc)
            return j['result']
        else:
            print(protocol.str_get_group_failed)

    # get_discus
    """
    {
        "retcode":0,
        "result":
            {
                "dnamelist":
                [
                    ...
                    {"name":"启陌、默契、ApopHasis","did":473848851},
                    ...    
                ]
            }
    }
    """

    def get_discus(self, psessionid, vfwebqq):
        url = protocol.url_get_discus.format(psessionid, vfwebqq, str(int(time.time() * 1000)))
        headers = protocol.headers_get_discus
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        if j["retcode"] == 0:
            print(protocol.str_get_discus_suc)
            return j['result']
        else:
            print(protocol.str_get_discus_failed)

    # self_info
    """
    {
        "retcode":0,
        "result":
            {
            "birthday":{"month":6,"year":1994,"day":26},
            "face":333,
            "phone":"",
            "occupation":"{occupation}",
            "allow":1,
            "college":"{college}",
            "uin":{uin},
            "blood":3,
            "constel":6,
            "lnick":"{lnick}",
            "vfwebqq":"{vfwebqq}",
            "homepage":"{homepage}",
            "vip_info":7,
            "city":"{city}",
            "country":"{country}",
            "personal":"{personal}",
            "shengxiao":11,
            "nick":"{nick}",
            "email":"",
            "province":"{province}",
            "account":{account},
            "gender":"male",
            "mobile":"150********"
            }
    }
    """

    def get_selfinfo(self):
        url = protocol.url_get_selfinfo.format(str(int(time.time() * 1000)))
        headers = protocol.headers_get_selfinfo
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        if j["retcode"] == 0:
            print(protocol.str_get_selfinfo_suc)
            return j['result']
        else:
            print(protocol.str_get_selfinfo_failed)

    # get_online
    """
    {
        "result":
        [
            ...
            {"client_type":2,"status":"online","uin":3637253110}
            ...    
        ],
        "retcode":0
    }
    """

    def get_online(self, vfwebqq, psessionid):
        url = protocol.url_get_online.format(vfwebqq, psessionid, str(int(time.time() * 1000)))
        headers = protocol.headers_get_online
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        if j["retcode"] == 0:
            print(protocol.str_get_online_suc)
            return j['result']
        else:
            print(protocol.str_get_online_failed)

    # get_recent
    """
    {
        "result":
        [
            ...
            {"type":2,"uin":473848851},
            ...
        ],
        "retcode":0
    }
    """

    def get_recent(self, vfwebqq, psessionid):
        url = protocol.url_get_recent
        headers = protocol.headers_get_recent
        payload = {'r': protocol.r_get_recent.format(vfwebqq, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        if j["retcode"] == 0:
            print(protocol.str_get_recent_suc)
            return j['result']
        else:
            print(protocol.str_get_recent_failed)

    # receive message

    # message
    """
    {
    "result":
        [
        {
        "poll_type":"message",
        "value":
            {
            "content":
                [
                    ["font",{"color":"000000","name":"微软雅黑","size":10,"style":[0,0,0]}],
                    "{content}"
                ],
            "from_uin":{from_uin},
            "msg_id":17382,
            "msg_type":1,
            "time":1513186825,
            "to_uin":{to_uin}
            }
        }
        ],
    "retcode":0}
    """

    # group message
    """
    {
    "result":
        [
        {
            "poll_type":"group_message",
            "value":
                {
                "content":
                    [
                        ["font",{"color":"000000","name":"微软雅黑","size":10,"style":[0,0,0]}],
                        "asd"
                    ],
                "from_uin":{group_code},
                "group_code":{group_code},
                "msg_id":4770,
                "msg_type":4,
                "send_uin":{send_uin},
                "time":1513185302,
                "to_uin":{self_qq}
                }
        }
        ],
    "retcode":0}
    """

    # discus message
    """
    {
    "result":
        [
        {
            "poll_type":"discu_message",
            "value":
                {
                "content":
                    [
                        [
                        "font",
                        {"color":"000000","name":"微软雅黑","size":10,"style":[0,0,0]}
                        ],
                        "1"
                    ],
                "did":{din},
                "from_uin":{din},
                "msg_id":4,
                "msg_type":5,
                "send_uin":{uin},
                "time":1515002365,
                "to_uin":{self_qq}
                }
        }
        ],
    "retcode":0
    }                
    """

    def poll(self, ptwebqq, psessionid):
        url = protocol.url_poll
        headers = protocol.headers_poll
        payload = {'r': protocol.r_get_recent.format(ptwebqq, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j

    # get friend info, will be called when receive a message and will only be called once.
    """
    {
    "retcode":0,
    "result":
        {
        "face":0,
        "birthday":
            {
            "month":{month},
            "year":{year},
            "day":{day}
            },
        "occupation":"",
        "phone":"",
        "allow":1,
        "college":"",
        "uin":{uin},
        "constel":6,
        "blood":0,
        "homepage":"",
        "stat":10,
        "vip_info":0,
        "country":"{country}",
        "city":"{city}",
        "personal":"",
        "nick":"{nick}",
        "shengxiao":11,
        "email":"",
        "client_type":1,
        "province":"河北",
        "gender":"male",
        "mobile":""
        }
    }
    """

    def get_friend_info_detail(self, friend_uin, vfwebqq, psessionid):
        url = protocol.url_get_friend_info_detail.format(str(friend_uin),
                                                         vfwebqq, psessionid, str(int(time.time() * 1000)))
        headers = protocol.headers_get_friend_info_detail
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    # get group info, will be called when receive a group message and will only be called once.
    """
    {
    "retcode":0,
    "result":
        {
        "stats":
            [
            {"client_type":1,"uin":120221673,"stat":10}
            ],
        "minfo":
            [
            {"nick":"启陌","province":"威斯康星","gender":"male","uin":592812090,"country":"美国","city":"迈迪逊"},
            {"nick":"ApopHasis","province":"河北","gender":"male","uin":120221673,"country":"中国","city":"石家庄"}
            ],
        "ginfo":
            {
            "face":0,
            "memo":"",
            "class":10011,
            "fingermemo":"",
            "code":1845372568,
            "createtime":1513196534,
            "flag":1090520065,
            "level":0,
            "name":"测试",
            "gid":1593634114,
            "owner":592812090,
            "members":
                [
                {"muin":592812090,"mflag":0},
                {"muin":120221673,"mflag":0}
                ],
            "option":2
            },
        "vipinfo":
            [
            {"vip_level":7,"u":592812090,"is_vip":1},
            {"vip_level":0,"u":120221673,"is_vip":0}
            ]
        }
    }
    """

    def get_group_info_detail(self, gcode, vfwebqq):
        url = protocol.url_get_group_info_detail.format(str(gcode), vfwebqq, str(int(time.time() * 1000)))
        headers = protocol.headers_get_group_info_detail
        self.session.headers.update(headers)
        result = self.session.get(url=url)
        j = result.json()
        return j

    # get discus info, will be called when receive a discus message and will only be called once.
    """
    {
    "result":
        {
        "info":
            {
            "did":1946609037,
            "discu_name":"启陌、默契、ApopHasis",
            "mem_list":
                [
                {"mem_uin":592812090,"ruin":592812090},
                {"mem_uin":120221673,"ruin":874318709},
                {"mem_uin":2449933433,"ruin":1821382625}
                ]
            },
        "mem_info":
            [
            {"nick":"启陌","uin":592812090},
            {"nick":"ApopHasis","uin":120221673},
            {"nick":"默契","uin":2449933433}
            ],
        "mem_status":
            [
            {"client_type":7,"status":"online","uin":592812090},
            {"client_type":1,"status":"online","uin":120221673}
            ]
        },
    "retcode":0
    }

    """

    def get_discus_info_detail(self, did, vfwebqq, psessionid):
        url = protocol.url_get_discus_info_detail.format(str(did), vfwebqq, psessionid, str(int(time.time() * 1000)))
        headers = protocol.headers_get_discus_info_detail
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

    # send group message
    def send_group_msg(self, group_uin, content, msg_id, psessionid):
        url = protocol.url_send_group_msg
        headers = protocol.headers_send_group_msg
        payload = {'r': protocol.r_send_group_msg.format(group_uin, content, msg_id, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j['retcode']

    # send discus message
    def send_discus_msg(self, did, content, msg_id, psessionid):
        url = protocol.url_send_discus_msg
        headers = protocol.headers_send_discus_msg
        payload = {'r': protocol.r_send_discus_msg.format(did, content, msg_id, psessionid)}
        self.session.headers.update(headers)
        result = self.session.post(url=url, data=payload)
        j = result.json()
        return j['retcode']

    def handle_msg(self, response):
        # msg from another user
        from_user = str(response['result'][0]['value']['from_uin'])
        if from_user == str(self.selfinfo_json['uin']):
            print(protocol.str_msg_from_self)
            return

        if from_user not in self.friends_info_detail.keys():
            j_tmp = self.get_friend_info_detail(from_user, self.info['vfwebqq'], self.info['psessionid'])
            if 'result' in j_tmp.keys():
                self.friends_info_detail[from_user] = {}
                self.friends_info_detail[from_user]["info"] = j_tmp['result']
                self.friends_info_detail[from_user]["index"] = random.randint(88000, 20000000)
                print(protocol.str_get_friend_info_succeeded)
            else:
                print(protocol.str_get_friend_info_failed)
                return
        # set msg index for each user

        handled, reply_content = self.stra_obj.get_msg_reply(response,
                                                             from_user, self.friends_info_detail[from_user]['info'])
        if not handled:
            return

        msg_index = self.friends_info_detail[from_user]['index']
        return_code = self.send_msg(from_user, reply_content, msg_index, self.info['psessionid'])
        if return_code == protocol.code_send_msg_suc:
            self.friends_info_detail[from_user]['index'] += 1
            print(protocol.str_send_msg_suc)
        else:
            print(protocol.str_send_msg_failed)

    def handle_group_msg(self, response):
        # msg from group
        from_group = str(response['result'][0]['value']['group_code'])
        sender_uin = str(response['result'][0]['value']['send_uin'])
        if sender_uin == str(self.selfinfo_json['uin']):
            print(protocol.str_msg_from_self)
            return
        if from_group not in self.group_info_detail.keys():
            j_tmp = self.get_group_info_detail(from_group, self.info['vfwebqq'])
            if 'result' in j_tmp.keys():
                self.group_info_detail[from_group] = {}
                self.group_info_detail[from_group]["info"] = j_tmp['result']
                self.group_info_detail[from_group]["index"] = random.randint(48000, 2000000)
                print(protocol.str_get_group_info_succeeded)
            else:
                print(protocol.str_get_group_info_failed)
                return
        # set group msg index

        handled, reply_content = self.stra_obj.get_group_reply(response, sender_uin, from_group,
                                                               self.group_info_detail[from_group]['info'])
        if not handled:
            return

        msg_index = self.group_info_detail[from_group]['index']
        return_code = self.send_group_msg(from_group, reply_content, msg_index, self.info['psessionid'])
        if return_code == protocol.code_send_group_msg_suc:
            self.group_info_detail[from_group]['index'] += 1
            print(protocol.str_send_group_msg_suc)
        else:
            print(protocol.str_send_group_msg_failed)

    def handle_discus_msg(self, response):
        # msg from discus
        from_discus = str(response['result'][0]['value']['did'])
        sender_uin = str(response['result'][0]['value']['send_uin'])
        if sender_uin == str(self.selfinfo_json['uin']):
            print(protocol.str_msg_from_self)
            return
        if from_discus not in self.discus_info_detail.keys():
            j_tmp = self.get_discus_info_detail(from_discus, self.info['vfwebqq'], self.info['psessionid'])
            if 'result' in j_tmp.keys():
                self.discus_info_detail[from_discus] = {}
                self.discus_info_detail[from_discus]["info"] = j_tmp['result']
                self.discus_info_detail[from_discus]["index"] = random.randint(1, 500)
                print(protocol.str_get_discus_info_succeeded)
            else:
                print(protocol.str_get_discus_info_failed)
                return
        # set discus msg index

        handled, reply_content = self.stra_obj.get_discus_reply(response, sender_uin, from_discus,
                                                                self.discus_info_detail[from_discus]['info'])
        if not handled:
            return

        msg_index = self.discus_info_detail[from_discus]['index']
        return_code = self.send_discus_msg(from_discus, reply_content, msg_index, self.info['psessionid'])
        if return_code == protocol.code_send_discus_msg_suc:
            self.discus_info_detail[from_discus]['index'] += 1
            print(protocol.str_send_discus_msg_suc)
        else:
            print(protocol.str_send_discus_msg_failed)

    def main_loop(self):
        print("in main loop...")

        while True:
            print("polling...")

            j = self.poll(self.info['ptwebqq'], self.info['psessionid'])
            if 'result' in j.keys() and j['result'][0]['poll_type'] == 'message':
                # msg from another user
                self.handle_msg(j)
            elif 'result' in j.keys() and j['result'][0]['poll_type'] == 'group_message':
                # msg from group
                self.handle_group_msg(j)
            elif 'result' in j.keys() and j['result'][0]['poll_type'] == 'discu_message':
                # msg from discus
                self.handle_discus_msg(j)
