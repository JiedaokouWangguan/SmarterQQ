# SmarterQQ QQBot based on SmartQQ

之前感觉挺好玩一直想做，前几天稍微空闲时间多就研究了一下。
对于qq机器人的协议的分析网上挺多的，但大部分是几年前的，有些依然管用，但有些已经被tx爸爸改了，对于没有修改的很多是借鉴[scienjus做的分析](http://www.scienjus.com/webqq-analysis-1/)。
[github](https://github.com/ScienJus/qqbot)

然后小部分代码，比如二维码的处理，借鉴了(wxBot)[https://github.com/liuwons/wxBot]

功能的话现在基本什么都不支持，后续开发会逐渐加上各种功能。

下面是对webQQ协议的一个简单的分析


自制qq机器人
功能还在持续开发中

已实现了模拟登陆
协议信息在protocol文件里
以后会写个清楚的

登陆后任一联系人向机器人发送消息会得到自动回复

储存cookie模块还没做，以后补上

因为腾讯爸爸把获得用户真正qq号的api封了所以真正实现qq群机器人还需要新算法

