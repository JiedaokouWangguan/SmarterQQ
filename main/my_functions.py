def msg_handler1(content, uin, user_detail):
    if content == "hello world":
        return True, "你好！"
    else:
        return False, ""


def msg_handler2(content, uin, user_detail):
    if content == "info":
        return True, "your uin is {}, your nick name is {}.".format(uin, user_detail['nick'])
    else:
        return False, ""


def group_msg_handler1(content, gin, sender_uin, group_info_detail):
    if content == "info":
        return True, "the group id is {}, the group's name is {}.".format(gin, group_info_detail['ginfo']['name'])
    else:
        return False, ""


def discus_msg_handler1(content, din, sender_uin, discus_info_detail):
    if content == "info":
        return True, "the discus id is {}, the discus's name is {}.".format(din,
                                                                            discus_info_detail['info']['discu_name'])
    else:
        return False, ""
