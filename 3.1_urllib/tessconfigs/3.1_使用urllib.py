# 爬虫最初的操作便是模拟浏览器向服务器发送请求，有了urllib库，只需关心请求的链接是什么，需要传的参数是什么，如何设置可选的
# 请求头即可，不用深入了解它到底是怎样传输和通信的，两行代码就可完成一个请求和响应的处理过程，得到网页内容。
# urllib是python内置的HTTP请求库，包含4个模块：
# request:是最基本的HTTP请求模块，用来模拟发送请求。就像在浏览器里输入网址然后回车一样，只需给库方法传入URL以及额外的参数
# error:异常处理模块，如果出现错误，可以捕获这些异常，进行重试或其他操作，保证程序不会以外终止
# parse:工具模块，提供许多URL处理方法，如拆分、解析、合并等
# robotparser：识别网站的robots.txt文件，判断哪些网站可以爬，用得比较少

# 1.发送请求：request模块，实现请求的发送并得到响应：
#   1>urlopen:urllib.request模块提供最基本的构造HTTP请求方法，可模拟浏览器的一个请求发起过程，还带有
#   处理授权验证(authentication)、重定向(redirection)、浏览器Cookies及其他内容
# 抓取Python官网：
# import urllib.request
#
# response = urllib.request.urlopen('https://www.python.org')
# print(response.read().decode('utf-8'))
# 仅用两行代码，输出了Python官网的源代码，利用type方法输出响应的类型：
# import urllib.request
#
# response = urllib.request.urlopen('https://www.python.org')
# print(type(response))
# 发现是一个HTTPResponse类型对象，主要包含read、readinto、getheader(name)、getheaders、fileno等方法，以及msg、version、
# status、reason、debuglevel、closed等属性，得到该对象后，可将它赋值给response变量，然后就可调用这些方法和属性，得到返回结果
# 如调用read可得到返回的网页内容，调用status可得到返回结果的状态码
# 利用urlopen方法，可得到简单网页的GET请求抓取
# 给链接传递一些参数，查看urlopen的API：
# urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
# A.data:可选，添加该参数，字节流编码格式(bytes)类型，需通过bytes方法转化，如传递该参数，请求方式改为POST：
# import urllib
# import urllib.request
#
# data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf-8')   # 传递参数word，值是hello，需被转为bytes类型
#                                             # 再用urllib.parse模块你的urlencode方法将参数字典转为字符串
# response = urllib.request.urlopen('http://httpbin.org/post', data=data)     # 指定编码格式，指定为utf-8，请求站点为
#                                             # httpbin.org，可提供HTTP请求测试,/post可测试POST请求，可输出请求的一些信息
#                                             # 传递的参数出现在了form字段中，表明模拟了表单提交方式，以POST方式传输数据
# print(response.read())

# B.timeout:设置超时时间，单位为秒，请求超出该时间，还没有得到响应，就抛出异常。如果不指定，默认使用全局默认时间
# import urllib.request
#
# response = urllib.request.urlopen('http://httpbin.org/get', timeout=1)
# print(response.read())
# 可通过设置这个超时时间来控制一个网页如果长时间未响应，就跳过它的爬取，可利用try except实现：
# import socket
# import urllib.request
# import urllib.error
#
# try:
#     response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)    # 请求测试链接，设置超时时间0.1秒
# except urllib.error.URLError as e:  # 捕获URLError异常
#     if isinstance(e.reason, socket.timeout): # 判断异常是socket.timeout类型，得出因为超时报仇
#         print('TIME OUT')

# C.其他用法：除了data参数和timeout参数，还有context参数，必须是ssl.SSLContext类型，指定SSL设置
# cafile和capath两个参数分别指定CA证书和路径，这个请求HTTPS链接时会有用
# cadefault参数弃用

# 2.Request:urlopen实现的只是最基本的请求，但不足以构建一个完整请求，如果请求中需要加入Headers等信息，利用Request构建
# import urllib.request
#
# request = urllib.request.Request('http://python.org')
# response = urllib.request.urlopen(request)  # 依然用urlopen方法发送骑牛，但参数不是url，而是Request类型对象
#                                             # 构造此数据结构，可将请求独立成一个对象，更加丰富和灵活地配置参数
# print(response.read().decode('utf=8'))
# # Request构造方法:
# class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
# url参数：请求URL，必传参数，其他都是可选参数
# data:必须传bytes类型，如果是字典，先用urllib.parse模块的urlencode编码
# headers是字典，就是请求头，可在构造请求时通过headers参数直接构造，也可通过调用请求是咧的add_headers方法添加
#               添加请求头最常见方法：修改User-Agent来伪装浏览器，默认User-Agent是Python-urllib
#               如伪装火狐浏览器：Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11
# origin_req_host是请求方的host名称或IP地址
# unverifiable：表示请求是否是无法验证的，默认False，即用户没有权限接收这个请求的结果。如请求一个HTML文档中的图片，但没有
#               自动抓取图像的权限，此时unverifiable的值就是True
# method是一个字符串，用来指示请求使用的方法，如GET、POST和PUT
# 传入多个参数构建请求：
from urllib import request, parse

url = 'http://httpbin.org'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
data = bytes(parse.urlencode(dict), encoding='utf-8')
req = request.Request(url=url, data=data, headers=headers, method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))
# 此外，headers也可用add_header方法来添加：
req = request.Request(url=url, data=data, method='POST')
req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')

# 3.高级用法：Handler，可理解为各种处理器，有专门处理登录验证的，有处理Cookies的，有处理代理设置的，几乎可以做到任何HTTP请求。
# urllib.request模块中的BaseHandler类，是所有其他Handler的父类，提供了最基本的方法，如default_open、protocol_request等
# 各种Handler子类继承这个BaseHandler类：
# HTTPDefaultErrorHandler：处理HTTP响应错误，错误会抛出HTTPError类型的异常
# HTTPRedirectHandler:处理重定向
# HTTPCookieProcessor:处理Cookie
# ProxyHandler:设置代理，默认代理为空
# HTTPPasswordMgr:管理密码，维护了用户名和密码的表
# HTTPBasicAuthHandler:管理认证，一个链接打开时需要认证，可用它来解决认证问题。
# 其他Handler类，可从参考官方文档：https://docs.python.org/3/library/urllib.request.html#urllib.request.BaseHandler
# 另一个类OpenerDirectior，称为Opener，urlopen方法就是urllir提供的一个Opener，使用更底层的实例来操作，用到Opener
# Opener可使用open方法，返回类型和urlopen相同，利用Handler来构建Opener

# 1)验证：提示输入用户名和密码，验证成功后才能查看页面，借助HTTPBasicAuthHandler就可以完成：
# from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
# from urllib.error import URLError
#
# username = 'username'
# password = 'password'
# url = 'http://localhost:5000/'
#
# p = HTTPPasswordMgrWithDefaultRealm() # 实例化HTTPBasicAuthHandler
# p.add_password(None, url, username, password) # 利用add_password添加用户名和密码，就建立了一个处理验证的Handler
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)   # 利用这个Handler并使用build_opener方法构建一个Opener，此Opener在发送时即验证成功
#
# try:
#     result = opener.open(url) # 利用Opener的open方法打开链接，即完成验证
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)

# 2)代理：添加代理：
# from urllib.error import URLError
# from urllib.request import ProxyHandler, build_opener
#
# proxy_handler = ProxyHandler({    # 使用了ProxyHandler，参数是一个字典，键名是协议类型，键值是代理链接，可添加多个代理
#     'http': 'http://127.0.0.1:9743',  # 本地搭建了一个代理，运行在9743端口
#     'https': 'https://127.0.0.1:9743'
# })
# opener = build_opener(proxy_handler)  # 利用此Handler及build_opener方法构造一个Opener，之后发送请求
# try:
#     response = opener.open('https://www.baidu.com')
#     print(response.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)

# 3)Cookies:

# import http.cookiejar, urllib.request
#
# cookie = http.cookiejar.CookieJar()   # 声明一个CookieJar对象
# handler = urllib.request.HTTPCookieProcessor(cookie)  # 利用HTTPCookiProcessor来构建一个Handler
# opener = urllib.request.build_opener(handler) # 利用build_opener构建出Opener
# response = opener.open('http://www.baidu.com')    # 执行open函数
# for item in cookie:
#     print(item.name+"="+item.value)   # 输出每条Cookie的名称和值

# filename = 'cookies.txt'
# cookie = http.cookiejar.MozillaCookieJar(filename)    # CookieJar需换成MozillaCookieJar，生成文件时会用到，CookieJar子类
                        # 处理Cookies和文件相关的事件，如读取和保存Cookies，将Cookies保存成Mozilla型浏览器的Cookies格式
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# cookie.save(ignore_discard=True, ignore_expires=True)

# LWPCookieJar同样可读取和保存Cookies，但保存的格式和MozillaCookiesJar不一样，会保存成libwww-perl(LWP)格式的Cookies文件
# cookie = http.cookiejar.LWPCookieJar(filename)
# 从文件中读取并利用：
# cookie = http.cookiejar.LWPCookieJar()    # 生成LWPCookieJar格式的Cookies，保存成文件
# cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)  # 调用load方法读取本地的Cookies文件，获取Cookies
# handler = urllib.request.HTTPCookieProcessor(cookie)  # 读取Cookies后，构建Handler
# opener = urllib.request.build_opener(handler) # 构建Opener
# response = opener.open('http://www.baidu.com')
# print(response.read().decode('utf-8'))

# urllib官方文档：https://docs.python.org/3/library/urllib.requeset.html#basehandler-objects
