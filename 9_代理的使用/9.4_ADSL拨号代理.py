# 如果追求更加稳定的代理，就需要购买专有代理或者自己搭建代理服务器，但是服务器一般都是固定的IP，ASDL动态拨号主机就派上用场了
# 1.ADSL：Asymmetric Digital Subscriber Line，非对称数字用户环路，它的上行和下行带宽不对称，采用频分复用技术把普通的电话线
# 分成了电话、上行和下行3个相对独立的信道，避免了相互干扰
# ADSL通过拨号方式上网，需要输入ADSL账号和密码，每次拨号就更换一个IP。IP分布在多个A段，如果IP都能用，意味着IP量级可达千万
# ADSL主机作为代理，每隔一段时间主机拨号就换一个IP，可以有效防止IP被封禁。稳定性很好，代理响应速度很快。

# 2.需要安装Redis数据库并启动服务、安装requests、redis-py、Tornado库

# 3.购买主机：购买一台动态拨号VPS主机，云立方：http://www.yunlifang.cn/dynamicvps.asp
# 选择电信线路，进入拨号主机的后台，预装一个操作系统，推荐CentOS 7系统
# 找到远程管理面板-远程连接的用户名和密码，就是SSH远程连接服务器的信息。如IP和端口是153.36.65.214:20063,用户名是root
# ssh root@153.36.65.214 -p 20063
# 进入后，发现一个可用的脚本文件ppp.sh,是拨号初始化的脚本。运行脚本，输入用户名和密码，开始拨号配置。
# 拨号测试前ping任何网站都是不通的，当前网络还没联通，输入adsl-start,再ping外网就可以通了
# 停止拨号：adsl-stop
# 断线重拨就是二者组合起来，先执行adsl-stop,再执行adsl-start
# ifconfig命令观察主机的IP，发现主机IP一直在变化，网卡名称ppp0

# 4.设置代理服务器：Linux下搭建HTTP代理服务器，推荐TinyProxy和Squid
#   4.1安装TinyProxy，系统使用CentOS，使用yum来安装，Ubuntu，使用apt-get安装
# yum install -y epel-release
# yum update -y
# yum install -y tinyproxy

#   4.2配置TineProxy：编辑配置文件，一般路径：/etc/tinyproxy/tinyproxy.conf
# 可以看到一行代码Port 8888,设置代理端口，默认8888
# Allow 127.0.0.1被允许链接的主机IP，希望连接任何主机，将这行代码注释即可
# 设置完成后，重启TinyProxy：systemctl enable tinyproxy.service      systemctl restart tinyproxy.service
# 防火墙开放该端口:iptables -I INPUT -p tcp --dport 8888 -j ACCEPT
# 直接关闭防火墙也可以：systemctl stop firewalld.service


#   4.3验证TinyProxy
# 用ifconfig查看当前主机IP,用curl命令设置代理请求httpbin，检测是否生效 curl -x 112.84.118.216 httpbin.org/get
# 如有正常的结果输出，且origin值为代理IP地址，证明TinyProxy配置成功

# 5.动态获取IP：在一台主机拨号切换IP的间隙代理是不可用的，在这拨号的几秒时间内如果有第二台顶替第一台主机，
# 可解决拨号间隙代理无法使用的问题，设计的架构必须要考虑支持多主机的问题
# 为了更加方便地使用代理，可以像代理池一样定义一个统一的代理接口，爬虫端只需配置代理接口即可获取可用代理，
# 搭建一个接口，就需要服务器，接口的数据从数据库选择，对每台主机的代理进行更新，更新需要拨号主机的唯一标识，
# 根据主机标识查出这条数据，然后将这条数据对应的代理更新
# 数据库端需要存储一个主机标识到代理的映射关系，关系型数据库，MySQL或Redis的Hash存储，只需存储一个映射关系，且Redis比MySQL好


# 6.存储模块：可被远程访问的Redis数据库，各个拨号机器只需要将各自的主机标识和当前IP和端口(代理)发送给数据库
# 定义操作Redis数据库的类
import redis
import random

# Redis数据库IP
REDIS_HOST = 'remoteaddress'
# Redis数据库密码，如无则填None
REDIS_PASSWORD = 'foobared'
# Redis数据库端口
REDIS_PORT = 6379
# 代理池键名
PROXY_KEY = 'adsl'


class RedisClient(object):  # 定义RedisClient类
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, proxy_key=PROXY_KEY):
        """
        初始化Redis连接
        :param host: Redis地址
        :param port: Redis端口
        :param password: Redis密码
        :param proxy_key: Redis散列表名
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.proxy_key = proxy_key

    def set(self, name, proxy): # 定义set方法，用来向散列表添加映射关系，从主机标识到代理的映射
        """
        设置代理
        :param name:主机名称
        :param proxy: 代理
        :return: 设置结束
        """
        return self.db.hset(self.proxy_key, name, proxy)   #散列表中存储key为adsl1、value为118.119.172:8888的映射

    def get(self, name):    # 从散列表中取出某台主机对应的代理
        """
        获取代理
        :param name:主机名称
        :return: 代理
        """
        return self.db.hget(self.proxy_key, name)

    def count(self):    # 返回当前散列表的大小，就是可用代理的数目
        """
        获取代理总数
        :return: 代理总数
        """
        return self.db.hlen(self.proxy_key)

    def remove(self, name): # remove方法从散列表中移除对应的主机的代理
        """
        删除代理
        :param name:主机名称
        :return: 删除结果
        """
        return self.db.hdel(self.proxy_keyj, name)

    def names(self):    # 获取散列表中的主机列表
        """
        获取主机名称列表
        :return: 获取主机名称列表
        """
        return self.db.hkeys(self.proxy_key)

    def random(self):   # 书籍从散列表中取出一个可用代理，类似代理池
        """
        随机获取代理
        :return:
        """
        proxies = self.proxies()
        return random.choice(proxies)

    def all(self):  # 主机代理映射
        """
        获取字典
        :return:
        """
        return self.db.hgetall(self.proxy_key)


# 7.拨号模块：拨号并把新的IP保存到Redis散列表里
# 拨号定时，分为定时拨号和非定时拨号
#   非定时拨号：向该主机发送一个信号，然后主机启动拨号，首先搭建一个重新拨号的接口，如搭建一个Web接口，请求该接口即进行拨号
#   开始拨号后，主机的状态就从在线转为离线，此时的Web接口相应失效了，拨号过程无法再连接，拨号后的IP也变了，无法通过接口来控制过程
#   和拨号结果，下次拨号还得改变拨号请求接口，开销较大
#   定时拨号：只需在拨号主机上运行定时脚本，每隔一段时间拨号一次，更新IP，将IP在Redis散列表中更新，调高拨号频率，减少IP被封可能


# 获取IP：拨号后的IP非常简单，只需调用ifconfig命令，解析出对应网卡的IP
# 还需进行有效性检测，拨号主机可以自己检测，利用requests设置自身代理请求外网，成功，再修改Redis散列表，更新代理
# 每台主机在拨号前需要将自身的代理从Redis散列表中移除
import re
import time
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from db import RedisClient

# 拨号网卡
ADSL_IFNAME = 'ppp0'
# 测试URL
TEST_URL = 'http://www.baidu.com'
# 测试超时时间
TEST_TIMEOUT = 20
# 拨号间隔
ADSL_CYCLE = 100
# 拨号出错重试间隔
ADSL_ERROR_CYCLE = 5
# ADSL命令
ADSL_BASH = 'adsl-stop;adsl-start'
# 代理运行端口
PROXY_PROT = 8888
# 客户端唯一标识
CLTENT_NAME = 'adsl1'

class Sender(): # 定义Sender类，作用是执行定时拨号，将新IP测试通过之后更新到远程Redis散列表里
    def get_ip(self, ifname=ADSL_IFNAME):   # 调用get_ip方法
        """
        获取本机IP
        :param ifname:网卡名称
        :return:
        """
        (status, output) = subprocess.getstatusoutput('ifconfig') # subprocess模块执行获取IP的命令ifconfig
        if status == 0:
            pattern = re.compile(ifname + '.*？inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
            result = re.search(pattern, output)
            if result:
                ip = result.group(1)
                return ip

    def test_proxy(self, proxy): # 调用test_proxy方法，将自身的代理设置好，使用requests库来用代理连接TEST_URL
        """
        测试代理
        :param proxy: 代理
        :return: 测试结果
        """
        try:
            response = requests.get(TEST_URL, proxies ={
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }, timeout = TEST_TIMEOUT)
            if response.status_code == 200:
                return True
        except (ConnectionError, ReadTimeout):
            return False

    def remove_proxy(self):
        """
        移除代理
        :return:None
        """
        self.redis = RedisClient()
        self.redis.remove(CLIENT_NAME)
        print('Successfully Removed Proxy')

    def set_proxy(self):    # 调用set_proxy方法将Redis散列表中本机对应的代理更新，设置时需要指定本机唯一标识和本机当前代理
        """
        设置代理
        :param proxy: 代理
        :return:
        """
        self.redis = RedisClient()
        if self.redis.set(CLIENT_NAME, proxy):  # 本机唯一标识可睡衣设置，对应变量为CLIENT_NAME，保证各台拨号主机不冲突即可
            # 调用RedisClient的set方法，参数name为本机唯一标识，proxy为拨号后的新代理，执行后可以更新散列表中的本机代理
            print('Successfully Set Proxy', proxy)

    def adsl(self): # 主方法是adsl方法，首先是一个无限循环，循环体内就是拨号的裸机价
        """
        拨号主进程
        :return:None
        """
        while True:
            print('ADSL Start, Remove Proxy, Please wait')
            self.remove_proxy() # 调用remove_proxy方法，将远程Redis散列表中本机对应代理移除，避免拨号本主机的残留代理被取到
            (status, output) = subprocess.getstatusoutput(ADSL_BASH) # 利用subprocess模块来执行拨号脚本，拨号命令ADSL_BASH
            if status == 0:
                print('ADSL Successfully')
                ip = self.get_ip()
                if ip:
                    print('Now IP', ip)
                    print('Testing Proxy, Please Wait')
                    proxy = '{ip}:{port}'.format(ip=ip, port=PROXY_PROT)
                    if self.test_proxy(proxy):
                        print('Valid Proxy')
                        self.set_proxy(proxy)
                        print('Sleeping')
                        time.sleep(ADSL_CYCLE)
                    else:
                        print('Invalid Proxy')
                else:
                    print('Get IP Failed, Re Dialing')
                    time.sleep(ADSL_ERROR_CYCLE)
            else:
                    print('ADSL Failed, Please Check')
                    time.sleep(ADSL_ERROR_CYCLE)

    def run():
        sender = Sender()
        sender.adsl()
# 至少配置两台主机，在一台主机的拨号间隙还有另一台主机的代理可用，拨号主机的数量不限，越多越好
# 首先移除代理，再进行拨号，拨号完成后获取新的IP，检测成功后设置到Redis散列表，等待一段时间再重新进行拨号
# 添加多态拨号主机，这样有多个稳定的定时更新的代理可用了。Redis散列表会实时更新各台拨号主机的代理

# 8.接口模块
# 和代理池一样，定义一些接口来获取代理，random获取随机代理，count获取代理个数
# 选用Tornado实现，利用Tornado的Server模块搭建Web接口服务
import json
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application

# API端口
API_PORT = 8000

class MainHandler(RequestHandler):
    def initialize(self, redis):
        self.redis = redis

    def get(self, api=''):
        if not api:
            links = ['random', 'proxies', 'names', 'all', 'count']  # 定义5个接口，random获取随机代理，names主机列表，
                                                                    # proxies代理列表，all代理映射，count代理数量
            self.write('<h4>Welcome to ADSL Proxy API</h4>')
            for link in links:
                self.write('<a href=' + link + '>' + link + '</a><br>')

        if api == 'random':
            result = self.redis.random()
            if result:
                self.write(result)

        if api == 'names':
            result = self.redis.names()
            if result:
                self.write(json.dumps(result))

        if api == 'proxies':
            result = self.redis.proxies()
            if result:
                self.write(json.dumps(result))

        if api == 'all':
            result = self.redis.all()
            if result:
                self.write(json.dumps(result))

        if api == 'count':
            self.write(str(self.redis.count()))

    def server(self, port=API_PORT, address=''):
        application = Application([
            (r'/', MainHandler, dict(redis=redis)),
            (r'/(.*)', MainHandler, dict(redis=redis)),
        ])
        application.listen(port, address=address)
        print('ADSL API Listening on', port)
        tornado.ioloop.IOLoop.instance().start()
# 访问proxies接口可获得所有代理列表
# 访问random接口可获取随机可用代理
# 将接口部署到服务器上，即可通过Web接口获取可用代理，获取方式和代理池类似。
# 代码地址：https://github.com/Python3WebSpider/AdslProxy
# ADSL拨号代理，可以无限次更换IP，且线路非常稳定，抓取效果好

