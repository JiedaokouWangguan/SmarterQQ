# SmarterQQ QQBot based on SmartQQ

之前感觉挺好玩一直想做，前几天稍微空闲时间多就研究了一下。
对于qq机器人的协议的分析网上挺多的，但大部分是几年前的，有些依然管用，但有些已经被tx爸爸改了，对于没有修改的协议内容，很多是借鉴[scienjus的微博](http://www.scienjus.com/webqq-analysis-1/)。

他的项目是用Ruby写的，地址在这[ScienJus/qqbot](https://github.com/ScienJus/qqbot)

然后小部分代码，比如二维码的处理，借鉴了[liuwons/wxBot](https://github.com/liuwons/wxBot)

功能的话现在基本什么都不支持，后续开发会逐渐加上各种功能。

下面是对webQQ协议的一个简单的分析

## 1.登陆
很久以前tx关闭了webQQ的账号密码登陆api，现在只能通过扫二维码登陆，在查资料的时候还发现了一个兄弟用qq空间的账号密码登陆的api先拿到一些cookie，再通过这个cookie登陆webQQ，没有具体研究，不过思路感觉很灵性。

### 1.1.拿二维码
在chrome的开发者工具里找到了得到二维码的请求，但意外的发现这个请求居然已经有cookie了，cookie包括两个key:pgv_pvi和pgv_si,而之前所有的包里都没有找到set-cookie，于是就去翻js，果然在一个request url是`https://tajs.qq.com/stats?sId=61651582`的请求的返回结果 \(是个js\)找到了对于pvg_pvi和pvg_si的赋值,是一个对于当前时间的随机函数：

    pgv_si = "s%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)
    pgv_pvi="%d" % int(round(2147483647 * random.random()) * + time.time() % 1E10)
  
拿到之后放到cookie里，接着设置一些header信息：

>Request URL:`https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=0.3188660334306206&daid=164&pt_3rd_aid=0`

>Referer:`https://xui.ptlogin2.qq.com/cgibin/xlogindaid=164&target=self&style=40&pt_disable_pwd=1&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001`

如果header设置不全非常容易返回错误信息。 

得到返回后从cookie里取出qrsig用来轮询二维码的扫描情况。

### 1.2.轮询二维码扫描情况，获取ptwebqq

这个轮询就是一遍遍地问服务器有没有设备去扫描刚才得到的二维码，这个请求的url是
> url:url = `ttps://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken={ptqrtoken}&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-{time_tag}&mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10232&login_sig=&pt_randsalt=0`

在这个url中我们需要两个变量，ptqrtoken和time_tag。ptqrtoken是用hash算出来的，hash的参数是刚才得到的qrsig，hash函数是通过一个request url是`https://imgcache.qq.com/ptlogin/ver/10232/js/c_login_2.js?max_age=604800&ptui_identifier=000D6ECCB81920246F7442F57BB50C2AB1B1F66F70CEC9568BAAFE32`的请求得到的\(在js里\)。用python写就是这样:

    def hash33(s):
        e = 0
        i = 0
        n = len(s)
        while n > i:
            e += (e << 5) + ord(s[i])
            i += 1
        return 2147483647 & e
        
对于time_tag，我看到的包基本都是从2290左右开始，然后每次增加大概2000。如果某次返回的json里面的状态码是0则证明验证成功，然后我们把cookie中的一个新值ptwebqq取出来。

### 1.3.获取vfwebqq

对于vfwebqq的请求较为简单
>url : `http://s.web2.qq.com/api/getvfwebqq?ptwebqq={ptwebqq}&clientid=53999199&psessionid=&t={time}`

其中ptwebqq刚才拿到了，time就填int(time.time()\*1000) \(webqq协议里面的时间大多都是这个\)。然后我们把cookie里的vfwebqq取出来。

### 1.4.获取psessionid，uin

这个请求比之前的tricky一点点

>url : `http://d1.web2.qq.com/channel/login2`
>headers :`{'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
           'Origin':'http://d1.web2.qq.com',
           'Host': 'd1.web2.qq.com',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded'}`
>payload : {'r':'{"ptwebqq":"{ptwebqq}","clientid":53999199,"psessionid":"","status":"online"}'}

之前的请求都是get，这是第一个post请求。需要注意的是payload，r的value是一个字符串，ptwebqq的value需要用引号括起来，clientid的value不能用引号扩。
然后我们就能从返回的json里拿到psessionid，uin了。



# 未完待续
街道口网管

12/11
