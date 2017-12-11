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
        self.selfinfo = {}

        pass

    # now we begin to get friends info, group info, discus info, selfinfo, online info, recent info
    def set_info(self, friend, group, discus, online, recent, selfinfo):
        self.friends_info = friend
        self.group_info = group
        self.discus_info = discus
        self.online_info = online
        self.recent_info = recent
        self.selfinfo = selfinfo

    def get_msg_reply(self, poll_json, user_info):
        result = "this is auto-replay, your nick name is {}.".format(user_info['nick'])
        return result