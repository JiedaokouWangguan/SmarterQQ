from smarterqq import smarter_qq
from smarterqq import strategy

stra_obj = strategy.Strategy()
sq = smarter_qq.SmarterQQ(stra_obj)
sq.main_loop()
