# SmarterQQ QQBot based on SmartQQ

之前感觉挺好玩一直想做，前几天稍微空闲时间多就研究了一下。
对于qq机器人的协议的分析网上挺多的，但大部分是几年前的，有些依然管用，但有些已经被tx爸爸改了，对于没有修改的很多是借鉴[scienjus做的分析](http://www.scienjus.com/webqq-analysis-1/),[ScienJus/qqbot](https://github.com/ScienJus/qqbot)

然后小部分代码，比如二维码的处理，借鉴了[liuwons/wxBot](https://github.com/liuwons/wxBot)

功能的话现在基本什么都不支持，后续开发会逐渐加上各种功能。

下面是对webQQ协议的一个简单的分析

## 登陆
很久以前tx关闭了webQQ的账号密码登陆api，现在只能通过扫二维码登陆，在查资料的时候还发现了一个兄弟用qq空间的账号密码登陆的api先拿到一些cookie，再通过这个cookie登陆webQQ，没有具体研究，不过思路感觉很灵性。

### 拿二维码
在chrome的开发者工具里找到了得到二维码的请求，但意外的发现这个请求居然已经有cookie了{cookie:pgv_pvi=4270682112; pgv_si=s9482312704},而之前所有的包里都没有找到set-cookie，于是就去翻js，果然在一个request url是`https://tajs.qq.com/stats?sId=61651582`的请求的返回结果 \(是个js\)找到了对于pvg_pvi和pvg_si的赋值,是一个对于当前时间的随机函数：

    pgv_si = "s%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)
    pgv_pvi="%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)
  
拿到之后放到cookie里，接着设置一些header信息：
Request URL:`https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=0.3188660334306206&daid=164&pt_3rd_aid=0`
Referer:`https://xui.ptlogin2.qq.com/cgibin/xlogindaid=164&target=self&style=40&pt_disable_pwd=1&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001`
如果header设置不全非常容易返回错误信息。 

