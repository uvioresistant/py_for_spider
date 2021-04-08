# 网站采取一些反爬虫措施:服务器检测某个IP在单位时间内的请求次数，超过某个阈值，服务器直接拒绝服务，返回错误信息如403，称为封IP
# 既然服务器检测的是某个IP单位时间的请求次数，name借助某种方式来伪装IP，让服务器无法识别由我们本机发起的请求，就可以防止封IP了
# 1.代理的设置
# 获取一个可用代理。搜索“代理”，会有很多免费代理，如西刺http://www.xicidaili.com/。但免费代理网站大多数都是不好用的
# 本机有相关代理软件，一般会在本机创建HTTP或SOCKS代理服务，直接使用此代理也可以
# 我的本机安装了一部代理软件，会在本地9743端口创建HTTP代理服务，即代理为127.0.0.1:9743,
# 还会在9742端口创建SOCKS代理服务，即代理为127.0.0.1:9742,只要设置了这个代理，就可以成功将本机IP切换到代理软件连接的服务器IP了
# 用上述代理来演示设置方法，可以自行替换成自己的可用代理。设置代理后测试网址http://httpbin.org/get
# 访问该网址可以得到请求的相关信息，其中origin字段就是客户端的IP，可以根据它来判断代理是否设置成功，即是否伪装了IP

# 2.urllib:最基础
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy = '127.0.0.1:9743'
proxy_handler = ProxyHandler({      # 借助ProxyHandler设置代理，参数是字典类型，键名为协议类型，键值是代理，
    'http': 'http://' + proxy,      # 此处代理前需要加上协议，http或https
    'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)    # 利用build_opener方法传入该对象来创建一个Opener，相当于此Opener已经设置好代理了
try:
    response = opener.open('http://httpbin.org/get')    # 直接调用Opener对象的open方法，即可访问我们所想要的链接
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
# 运行输出结果是一个JSON，有一个字段origin，标明了客户端的IP，验证一下，此处IP确实为代理IP，不是真实IP

# 如遇到需要认证的代理，可以用如下方法设置：
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy = 'username:password@127.0.0.1:9743'  # 改变的只是proxy变量，只需在代理前面加入代理认证的用户名密码即可
proxy_handler = ProxyHandler({
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)
try:
    response = opener.open('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)

# 代理是SOCKS5类型：
import socks
import socket
from urllib import request
from urllib.error import URLError

socks.get_default_proxy(socks.SOCKS5, '127.0.0.1', 9742)
socket.socket = socks.socksocket
try:
    response = request.rulopen('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
# 结果中origin字段同样为代理的IP

# 3.requests：代理设置更加简单，只需传入proxies参数
import requests

proxy = '127.0.0.1:9743'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
# requests代理设置比urllib简单很多，只需要构造代理字典，然后通过proxies参数即可，不需要重新构建Opener

# 如果代理需要认证，同样在代理前面加上用户名密码即可，

# 使用SOCKS5代理：
import requests

proxy = '127.0.0.1:9742'
proxies = {
    'http': 'socks5://' + proxy,
    'http': 'socks5://' + proxy
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
# 需要额外安装模块requests[socks],
# 另外还有一种设置方式，和urllib方法相同，使用socks模块，需要像上文一样安装socks库
import requests
import socks
import socket

socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9742)
socket.socket = socks.socksocket
try:
    response = requests.get('http://httpbin.org/get')
    print(response.text)
except requests.exceptionis.ConnectionError as e:
    print('Error', e.args)
# 此方法也可以设置SOCKS5代理，相比第一种方法，此方法是全局设置

# 4.Selenium
# Chrome设置方法：
from selenium import webdriver

proxy= '127.0.0.1:9743'
chrome_options = webdriver.ChromeOptions()  # 通过ChromeOptions设置代理，创建chrome_options参数传递
chrome_options.add_argument('--proxy-server=http://' + proxy)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://httpbin.org/get')

# 若代理是认证代理，设置方法比较麻烦：
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile

ip = '127.0.0.1'
port = 9743
username = 'foo'
password = 'bar'

manifest_json = """     # 在本地创建一个manifest.json配置文件
{
    "version": "1.0.0",
    manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequests",
        "webRequestBlocking"
    ],
    "background": {
        "scripts: ["background.js"]
    }
}
"""

background_js = """     # 在本地创建background.js脚本来设置认证代理
var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
             scheme: "http",
             host: "%(ip)s",
             port: %(port)s
             }
         }
     }
     
chrome.proxy.settings.set({value: config, scope: "regular"}， function() {});

function callbackFn(details) {
    return {
    authCredentials: {
        username: "%(username)s",
        password: "%(password)s"
        }
    }
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
)
""" % {'ip': ip, 'port': port, 'username': username, 'password': password}

plugin_file = 'proxy_auth_plugin.zip'   # 运行代码后，本地会生成一个proxy_auth_plugin.zip文件来保存当前配置
with zipfile.ZipFile(plugin_file, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("backgroud.js", background_js)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_extension(plugin_file)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://httpbin.org/get')

# 对于PhantomJS来说，代理设置方法可借助service_args参数
# from selenium import webdriver
#
# service_args = [
#     '--proxy=127.0.0.1:9743',
#     '--proxy-type=http'
# ]
# browser = webdriver.PhantomJS(service_args=service_args)
# browser.get('http://httpbin.org/get')
# print(browser.page_source)
# 使用service_args参数，将命令行的一些参数定义为列报表，初始化时传递给PhantomJS对象即可
# 如需认证，只需要加入--proxy-auth选项即可
# service_args = [
#     '--proxy=127.0.0.1:9743',
#     '--proxy-type=http',
#     '--proxy-auth=username:password'
# ]
# 代码地址：https://github.com/Python3WebSpider/ProxySettings

