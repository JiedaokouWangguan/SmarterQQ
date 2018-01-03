#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module controls the actual behavior of the program """

__author__ = 'JiedaokouWangguan'


class Strategy(object):

    def __init__(self):
        self.friends_info = {}
        self.group_info = {}
        self.discus_info = {}
        self.online_info = {}
        self.recent_info = {}
        self.self_info = {}

        self.friends_info_detail = {}
        self.group_info_detail = {}
        self.discus_info_detail = {}

        self.strategy_msg = []
        self.strategy_group_msg = []
        self.strategy_discus_msg = []

    # now we begin to get friends info, group info, discus info, selfinfo, online info, recent info
    def set_info(self, friend, group, discus, online, recent, selfinfo):
        self.friends_info = friend
        self.group_info = group
        self.discus_info = discus
        self.online_info = online
        self.recent_info = recent
        self.self_info = selfinfo

    def get_msg_reply(self, poll_json, uin, user_info_detail):
        self.friends_info_detail[uin] = user_info_detail
        for func in self.strategy_msg:
            content = str(poll_json['result'][0]['value']['content'][1])
            handled, result = func(content, uin, user_info_detail)
            if handled:
                return handled, result
        return False, ""

    def get_group_reply(self, poll_json, gin, sender_uin, group_info_detail):
        self.group_info_detail[gin] = group_info_detail
        for func in self.strategy_group_msg:
            content = str(poll_json['result'][0]['value']['content'][1])
            handled, result = func(content, gin, sender_uin, group_info_detail)
            if handled:
                return handled, result
        return False, ""

    def get_discus_reply(self, poll_json, din, sender_uin, discus_info_detail):
        self.discus_info_detail[din] = discus_info_detail
        for func in self.strategy_discus_msg:
            content = str(poll_json['result'][0]['value']['content'][1])
            handled, result = func(content, din, sender_uin, discus_info_detail)
            if handled:
                return handled, result
        return False, ""

    def get_strategy_msg(self):
        return self.strategy_msg

    def add_strategy_msg(self, func):
        self.strategy_msg.append(func)

    def get_strategy_group_msg(self):
        return self.strategy_group_msg

    def add_strategy_group_msg(self, func):
        self.strategy_group_msg.append(func)

    def get_strategy_discus_msg(self):
        return self.strategy_discus_msg

    def add_strategy_discus_msg(self, func):
        self.strategy_discus_msg.append(func)
