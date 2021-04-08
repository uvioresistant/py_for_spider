# 没有登录的情况下，也可以访问一部分页面或者请求一些接口，网站本身需要做SEO，不会对所有页面都设置登录限制
# 不登录爬取弊端：
# a.设置了登录限制页面无法爬取：论坛设置登录才可查看资源，博客设置登录才可查看全文
# b.一些页面和端口虽然可以直接请求，但是请求频繁就容易被限制或封IP，登录后就不会出现问题，即被反爬的可能性更低
# 微博为例做实验，新浪财经官方微博的信息接口https://m.weibo.cn/api/container/getIndex?uid=1638782947&luicode=20000174
# &type=uid&value=1638782947&containerid=1005051638782947,浏览器直接访问，返回数据是JSON格式，直接解析JSON即可提取信息
# 但接口没登录情况下会有请求频率检测，一段时间内访问太过频繁，如一直刷新，会看到请求频率过高
# 重新打开，登录微博账号后，正常显示；一直用同一个账号频繁请求，就有可能遇到请求过于频繁而封号的问题
# 做大规模爬取，需要拥有很多账号，每次请求随机选取一个账号，降低单个账号的访问频率，被封几率大大降低
# 用Cookies池维护多个账号的登录信息

# 1.目标：新浪微博实现Cookies池的搭建过程。Cookies池保存许多新浪微博账号和登录后的Cookies信息，且Cookies池需定时检测每个
# Cookies的有效性，如果Cookies无效，删除该Cookies并模拟登录生成新的Cookies。
# 还需要重要接口，获取随机Cookies的接口，Cookies运行后，请求该接口，可随机获得一个Cookies并用其爬取
# Cookies池需要自动生成Cookies、定时检测Cookies、提供随机Cookies几大核心功能

# 2.准备工作：一些微博账号，安装Redis数据库，Python的redis-py、requests、Selenium和Flask库，安装Chrome浏览器并配置Driver

# 3.Cookies池构架：和代理池类似，4个核心模块：获取模块~~~存储模块~~~检测模块~~~接口模块
# 存储模块：存储每个账号的用户名密码及对应的Cookies，提供方法实现方便的存取操作
# 生成模块：生成新的Cookies，从存储模块逐个拿去账号用户名和密码，模拟登录目标页面，判断登录成功，将Cookies返回交给存储模块存储
# 检测模块：定时检测数据库中Cookies，需设置检测链接，不同站点检测链接不同，逐个拿取账号对应Cookies请求链接，返回状态失效移除
# 接口模块：用API提供对外服务接口，可用Cookies可能有多个，随机返回Cookies的接口，保证每个Cookies都可能被取到，Cookies越多，
#           每个Cookies取到的概率就越小，检测被封号的风险。

# 4.Cookies池的实现：
# 存储模块：存成用户名和密码的映射。Cookies存成JSON字符串，同时保存Cookies对应的用户名信息，也是用户名和Cookies的映射
# 两组映射，用Redis的Hash，建立两个Hash：用户名密码Hash结构、用户名Cookies Hash结构
# Hash的Key就是账号，Value对应密码或者Cookies。另外Cookies需要做到可扩展，存储的账号和Cookies不单单只有微博，其他站同样可以
# Hash的名称可以做二级分类。存账号的Hash名称为accounts:weibo,Cookies的Hash名称为cookies：weibo
# 创建存储模块类，提供Hash的基本操作：
import random
import redis

class RedisClient(object):  # 新建一个RedisClient
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWORD): # 初始化__init__方法
        """
        初始化Redis连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type    # 有两个关键参数type和website，分别代表类型和站点名称，用来拼接Hash名称的两个字段
        self.website = website  # 如果存储账户的Hash，此处type为accounts、website为weibo；
                                # 存储Cookies的Hash，type为cookies，website为weibo

def name(self):
    """
    获取Hash的名称
    :return: Hash名称
    """
    return "{type}:{website}".format(type=self.type, website=self.website)  # name方法凭借了type和website，组成Hash名称

def set(self, username, value): # set方法代表设置某个键值对
    """
    设置键值对
    :param username: 用户名
    :param value: 密码或Cookies
    :return:
    """
    return self.db.hset(self.name(), username, value)

def get(self, usesrname):   # get方法代表获取某个键值对
    """
    根据键名获取键值
    :param usesrname: 用户名
    :return:
    """
    return self.db.hget(self.name(), username)

def delete(self, username): # delete方法删除Hash的某个键值对
    """
    根据键名删除键值对
    :param username: 用户名
    :return: 删除结果
    """
    return self.db.hdel(self.name(), username)

def count(self):    # count获取Hash长度
    """
    获取数目
    :return: 数目
    """
    return self.db.hlen(self.name())

def random(self):   # 比较重要的random方法，用于从Hash里随机选取一个Cookies并返回，与接口模块对接可实现请求接口
    """
    随机得到键值，用于随机Cookies获取
    :return: 随机Cookies
    """
    return random.choice(self.db.hvals(self.name()))

def usernames(self):
    """
    获取所有账户信息
    :return: 所有用户名
    """

def all(self):
    """
    获取所有键值对
    :return: 用户名和密码或Cookies的映射表
    """
    return self.db.hgetall(self.name())


# 生成模块：负责获取各个账号信息并模拟登录，随后生成Cookies并保存，首先获取两个Hash的信息，看账户Hash比Cookies的Hash多了哪些
# 还没有生成Cookies的账号，将剩余的账号遍历，再去生成Cookies即可
for username in accounts_usernames:
    if not username in cookies_usernames:
        password = self.accounts_db.get(username)
        print('正在生成Cookies', '账号', username, '密码', password)
        result = self.new_cookies(username, password)
# 对接的是新浪微博，已破解新浪微博的四宫格验证码，直接对接即可，需要加一个获取Cookies的方法：
def get_cookies(self):
    return self.browser.get_cookies()

def main(self):
    self.open()
    if self.password_error():
        return {        # 返回结果的类型是字典，且附有状态码status，根据不同状态码做不同的处理
            'status': 2,
            'content': '用户名或密码错误'
        }
    # 如果不需要验证码直接登录成功
    if self.login_successfully():
        cookies = self.get_cookies()
        return {
            'status': 1,
            'content': cookies
        }
    # 获取验证码图片
    image = self.get_image('captcha.png')
    numbers = self.detect_image(image)
    self.move(numbers)
    if self.login_successfully():
        cookies = self.get_cookies()
        return {
            'status': 1,
            'content': cookies
        }
    else:
        return {
            'status': 3,         # 代表登录失败的一些错误，不能判断是否用户名或密码错误，不能成功获取Cookies，进行下一个处理
            'content': '登录失败'
        }

result = self.new_cookies(username, password)   # 扩展其他站点，只需实现new_cookies方法即可，返回对应的模拟登录记过
# 成功获取
if result.get('status') == 1:
    cookies = self.process_cookies(result.get('content'))
    print('成功获取到Cookies', cookies)
    if self.cookies_db.set(username, json.dumps(cookies)):
        print('成功保存Cookies')
# 密码错误，移除账号
elif result.get('status') == 2:
    print(result.get('content'))
    if self.accounts_db.delete(username):
        print('成功删除账号')
else:
    print(result.get('content'))
# 代码运行后会遍历一次尚未生成Cookies的账号，模拟登录生成新的Cookies


# 检测模块：免不了Cookies失效问题，如果时间太长导致Cookies失效，或Cookies使用频繁导致无法正常请求网页，不能让它继续保存在数据库
# 增加定时检测模块，负责遍历池中所有Cookies，设置对应的检测链接，用一个个Cookies请求这个链接，成果，或状态码合法，该Cookies有效
# 请求失败或无法获取正常数据，跳回登录页面或跳到验证页面，此Cookies无效，将该Cookies从数据库中移除
# 此Cookies移除后，生成模块会用此账号重新登录，此账号的Cookies被重新更新
# 实现通用可扩展性，首先定义一个检测器的父类，声明一些通用组件
class ValidTester(object):  # 定义了一个父类ValidTester
    def __init__(self, website='default'):  # __init方法里指定站点名称website
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)  # 存储模块连接对象cookies_db: 负责操作Cookies的Hash
        self.accounts_db = RedisClient('accunts', self.website) # accounts_db：负责操作账号的Hash

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):  # run方法是入口
        cookies_groups = self.cookies_db.all()
        for usernamecookies in cookies_groups.items():  # 遍历所有的Cookies
            self.test(username, cookies)    # 调用test方法测试，需重写子类来实现test方法，需加一个子类继承ValidTester

import json
import requests
from requests.exceptions import ConnectionError

class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):      # test方法将Cookies转化字典，检测Cookies格式，
        print('正在测试Cookies', '用户名', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:               # 格式不正确，直接删除
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
    try:
        test_url = TEST_URL_MAP[self.website]   # 拿此Cookies请求被检测的URL，test方法检测微博，检测的URL可以是某个Ajax接口
        response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False) # 用Cookies请求目标站点，禁止
                # 重定向和设置超时时间，得到响应之后检测其返回状态码
        if response.status_code == 200: # 直接返回200状态码，则Cookies有效
            print('Cookies有效', username)
            print('部分测试结果', response.text[0:50])
        else:
            print(response.status_code, response.headers)   # 跳转到登录页面，则Cookies已失效
            print('Cookies失效', username)
            self.cookies_db.delete(username)    # 如果Cookies失效，将其从Cookies的Hash里移除即可
            print('删除Cookies', username)
    except ConnectionError as e:
        print('发生异常', e.args)
# 为了实现可配置化，将测试URL也定义成字典：
TEST_URL_MAP = {
    'weibo': 'https://m.weibo.cn/'
}

# 接口模块：Cookies池最终还是需要给爬虫来用，同事一个Cookies池供多个爬虫使用，需要定义一个Web接口，爬虫访问接口得到随机Cookies
# 采用Flask实现接口的搭建:
import json
from flask import Flask, g
app = Flask(__name__)
# 生成模块的配置字典
GENERATOR_MAP = {   # 接口字段定义为站点名称
    'weibo': 'WeiboCookiesGenerator'
}
@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'

def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website +'")'))
    return g

@app.route('/<website>/random')
def random(website):    # 第二个字段定义为获取的方法
    """
    获取随机的Cookie，访问地址如 /weibo/random
    :return: 随机的Cookie
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies

# 调度模块：让几个模块配合运行起来，主要工作就是驱动几个模块定时运行，同时各个模块需要在不同进程上运行
import time
form multiprocessing import Process
from cookiespool.api import app
from cookiespool.config import *
from cookiespool.generator import *
from cookiespool.tester import *

class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Cookies检测进程开始运行')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')  # 利用eval动态新建各个类的对象，
                    tester.run()
                    print('Cookies检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                    print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Cookies生成进程开始运行')
            try:
                for website, cls in GENERATOR_MAP.items):
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Cookies生成完成')
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API接口开始运行')
        app.run(host=API_HOST, port=API_PORT)   # 调用run运行

    def run(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api) # Scheduler将字典进行遍历，
            api_process.start()

        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)  # 多进程使用multiprocessing中的Process类
            valid_process.start()       # 调用start方法即可启动各个经常
# 用到两个重要的配置，参数模块类和测试模块类的字典配置
# 参数模块类：拓展其他站点，在此配置
GENERATOR_MAP = {       # 为了方便动态拓展使用，键名为站点名称，键值为类名
    'weibo': 'WeiboCookiesGenerator'
    #'zhihu': 'ZhihuCookiesGenerator' 配置其他站点可在字典中添加，拓展知乎站点的产生模块
}

# 测试模块类，拓展其他站点，在此配置
TESTER_MAP = {
    'weibo': 'WeiboValidTester'
}

# 各个模块还设有模块开关，可以在配置文件中只有设置开关的开启和关闭：
# 产生模块开关
GENERATOR_PROCESS = True
# 验证模块开关
VALID_PROCESS = False
# 接口模块开关
API_PROCESS = True

# 将模块同时开启，启动调度器，各个模块并行运行，互不干扰
# 可以访问接口获取随机的Cookies，爬虫只需请求该接口就可以实现随机Cookies的获取
# 代码地址：https://github.com/Python3WebSpider/CookiesPool