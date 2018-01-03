from smarterqq import smarter_qq
from smarterqq import strategy
from smarterqq.main.my_functions import *

stra_obj = strategy.Strategy()

# add msg handler
stra_obj.add_strategy_msg(msg_handler1)
stra_obj.add_strategy_msg(msg_handler2)

# add group msg handler
stra_obj.add_strategy_group_msg(group_msg_handler1)

# add discus msg handler
stra_obj.add_strategy_discus_msg(discus_msg_handler1)

sq = smarter_qq.SmarterQQ(stra_obj)
sq.main_loop()
