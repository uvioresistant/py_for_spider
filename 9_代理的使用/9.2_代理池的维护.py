# 网上有大量公开的免费代理，也可以购买付费的代理IP，需要提前做筛选，将不可用的代理剔除掉，保留可用代理，搭建一个高效易用的代理池
# 1.准备工作：成功安装Redis数据库并启动服务，安装aiohttp、requests、redis-py、pyquery、Flask库

# 2.代理池的目标：存储模块：存储抓取下来的代理。保证不重复，标识可用情况，动态实时处理每个代理；用Redis的SortedSet有序集合
#                获取模块：定时在各大代理网站抓代理。代理形式都是IP+端口，从不同来源获取，抓取高匿代理，成功后保存到数据库中
#                检测模块：定时检测数据库中的代理，设置一个检测代理，标识每个代理的状态，设置分数，100分可用，辨识代理可用情况
#                接口模块：用API提供对外服务接口，可直接连接数据库，但不安全，比较安全和方便的方式是提供一个WebAPI，负载均衡

# 3.代理池的构架：
#     存储模块：用Redis的有序集合，做代理的去重和状态标识，也是中心模块和基础模块，将其他模块串联起来
#     获取模块：定时从代理网站获取代理，将火气的代理传递给存储模块，并保存到数据库
#     检测模块：定时通过存储模块获取所有代理，并对代理进行检测，根据不同的检测结果对代理设置不同标识
#     接口模块：通过WebAPI提供服务接口，接口通过连接数据库并通过Web形式返回可用代理

# 4.代理池的实现：
#       存储模块：使用Redis的有序集合，集合的每一个元素都是不重复的，集合的元素就成了一个个代理，就是IP+端口的形式；
#                   有序集合的每一个元素都有一个分数字段，分数是可以重复的，可以是浮点数类型，也可以是整数类型
#                   该集合会根据每一个元素的分数对集合进行排序，数值小的排在前面，大的在后，可以实现集合元素的排序了
#                     分数可以作为判断一个代理是否可用的标志，100为最高分，代表最可用，0为最低分，最不可用。
#                     获取可用代理，可从代理池中随机获取分数最高的代理，保证每个可用代理都会被调用到
#                 分数是判断代理稳定性的重要标准，规则：
#                     100为可用，检测器定时循环检测每个代理可用情况，检测到可用立即设置100，不可用分数减1，减至0代理移除
#                     尝试机会越多，代理拯救回来的机会越多，就不容易将曾经的一个可用代理丢弃，代理不可用的原因可能是网络繁忙
#                  新获取的代理的分数设置为10，不可用就减1，减到0，就移除；如果代理可用，分数就置为100


# 定义一个类来操作库的有序集合，定义一些方法来实现分数的设置、代理的获取
MAX_SCORE = 100     # 定义常量，最大分数
MIN_SCORE = 0       # 最小分数
INITIAL_SCORE = 10  # 初始分数
REDIS_HOST = 'localhost'    # Redis的连接信息，地址
REDIS_PORT = 6379           # 端口
REDIS_PASSWORD = None       # 密码
REDIS_KEY = 'proxies'       # 有序集合的键名

import redis
from random import choice


class RedisClient(object):      # 定义RedisClient类，可用来操作Redis的有序集合，定义方法对集合中的元素进行处理
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):  # 初始化StrictRedis类，建立Redis连接
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):      # 向数据库添加代理并设置分数，
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):    # 默认INITIAL_SCORE,就是10
            return self.db.zadd(REDIS_KEY, score, proxy)     # 返回结果是添加的结果

    def random(self):   # 首先获取100的代理，随机选择一个返回
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):  # 代理检测无效设置分数减1，代理传入后，将代理的分数减1，分数达到最低值，代理就删除
        """
        代理值减一分，分数小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用， 设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zadd(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

# 获取模块：定义一个Crawler从各大网站抓取代理
import json
from .utils import get_page
from pyquery import PyQuery as pq

class ProxyMetaclass(type):     # 借助元类来实现ProxyMetaclass，
    def __new__(cls, name, bases, attrs):   # Crawl类将它设置为元类，实现了__new__方法,第四个参数attrs中包含了类的属性
        count = 0
        attrs['__CrawlFunc__'] == []
        for k, v in attrs.items():  # 遍历attrs参数可获取类的所有方法信息，遍历字典一样，键名对应方法的名称
            if 'crawl_' in k:   # 判断方法的开头是否crawl，
                attrs['__CrawlFunc__'].append(k)    # 是，则将其加入到__CrawFunc__属性中
                count += 1
        attrs['__CrawlFuncCount__'] = count     # 成功将所有以crawl开头的方法定义成了一个属性
        return type.__new__(cls, name, bases, attrs)    # 动态获取到所有以crawl开头的方法列表
# 要做扩展，只需要添加一个以crawl开头的方法。抓取快代理，只需要在Crawler类中增加crawl_kuaidaili方法，仿照其他几个方法
# 将其定义成生成器，抓取其网站的代理，然后通过yield返回代理即可。

class Crawler(object, metaclass=ProxyMetaclass):    # 将获取代理的每个方法统一定义为以crawl开头，拓展时只添加crawl开头即可
    def get_proxies(self, callback):    # 定义一个get_proxies方法，
        proxies = []
        for proxy in eval("self.{}()".format(callback)):    # 将所有crawl开头的方法调用一遍
            print('成功获取到代理', proxy)     # 获取每个方法返回的代理并组合成列表形式
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):  # 抓取代理66免费代理网站
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)    # 程序首先获取网页
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)'.text)
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])      # 通过yield返回一个个代理

    def crawl_proxy360(self):      # 抓取Proxy360免费代理网站
        """
        获取Proxy360
        :return: 代理
        """
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBoottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])

    def crawl_goubanjia(self):  # 抓取Goubanjia免费代理网站
        """
        获取Goubanjia
        :return: 代理
        """
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ',' ')
# 程序首先获取网页，然后用pyquery解析，解析出IP加端口的形式的代理形式返回


# 定义Getter类，用来动态调用所有以crawl开头的方法，获取抓取到的代理，加入到数据库存储起来
from db import RedisClient
from crawler import Crawler

POOL_UPPER_THRESHOLD = 10000    # 代表代理池的最大数量

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):    # is_over_threshold方法判断代理池是否达到了容量阈值
        """
        判断是否达到了代理池限制
        :return:
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:  # 调用RedisClient的count方法来获取代理的数量，进行判断，
            return True     # 达到阈值，返回True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():    # 判断代理池是否达到阈值
            for callback_label in range(self.crawler.__CrawlFuncCount__):   # 调用了Crawler类的__CrawlFunc__属性
                callback = self.crawler.__CrawlFunc__[callback_label]   # 获取到所有以crawl开头的方法列表
                proxies = self.crawler.get_proxies(callback)    # 依次通过get_proxies方法调用
                for proxy in proxies:   # 得到各个方法抓球到的代理
                    self.redis.add(proxy)   # 利用RedisClient的add方法加入数据库


# 检测模块：对所有代理进行多轮检测，代理检测可用，分数设置为100，不可用，分数减1，可实时改变每个代理的可用情况
# 获取有效代理只需要获取分数高的代理即可
# 异步请求库aiohttp进行检测
# requests为同步请求库，发出请求后，程序需要等待网页加载完成后才能继续执行。这个过程会阻塞等待响应
# 异步请求库解决了这个问题，类似JS中的回调，请求发出后，程序可以继续执行去做其他事情，响应到达时，程序再去处理这个响应，没有阻塞
# 可以充分利用时间和资源，大大提高效率。检测一个代理一般需要十多秒甚至几十秒的时间，使用aiohttp异步请求库，效率提升几十倍


VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100   # 设置批量测试的最大值为100，即一批测试最多100个，避免代理池过大，一次性测试导致内存开销过大的问题

class Tester(object):   # 定义一个类Tester
    def __init__(self):
        self.redis = RedisClient()  # 建立一个RedisClient对象，供该对象中其他方法使用

    async def test_single_proxy(self):  # 定义test_single_proxy方法，检测单个代理的可用情况，参数就是被检测的代理,async异步
        """
        测试单个代理
        :param proxy: 单个代理
        :return:  None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:    # 创建aiohttp的ClientSession对象，
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response: # 通过proxy传递get方法
                    # 测试的链接定义为常量TEST_URL,对某个网站有抓取需求，将TEST_URL设置为目标网站地址
                    if response.status in VALID_STATUS_CODES:   # 定义VALID_STATUS_CODES变量，是列表形式，包含正常状态码
                        self.redis.max(proxy)   # 调用RedisClient的max方法将代理分数设置为100
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)  # 否则调用decrease方法将代理分数减1
                        print('请求相应码不合法', proxy)
            except (ClientError, ClientConnectorError, TimeoutError, AttributeError):
                self.redis.decrease(proxy)  # 出现异常也同样将代理分数减1
                print('代理请求失败', proxy)

    def run(self):
        """
        测试主函数
        :return: None
        """
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            # 批量测试
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)


# 接口模块：为了使代理池作为一个独立服务运行，增加一个接口模块，以Web API形式暴露可用代理，获取代理只需请求接口即可
# 可以避免以下弊端：
# a.其他人使用代理池，需要知道Redis连接的用户名和密码信息，不安全
# b.代理池需要部署在远程服务器上运行，而远程服务器的Redis只允许本地连接，就不能远程直连RedisClient来获取代理
# c.RedisClient类或者数据库结构有更新，爬虫端必须同步更新，非常麻烦

# 使用轻量级库Flask来实现接口模块
from flask import Flask, g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient() # 声明Flask对象，定义3个接口
    return g.redis

@app.route('/')
def index():    # 定义接口：首页
    return '<h2>Welcome to Procxy Pool System</h2>'

@app.route('/random')   # 定义接口：随机代理页
def get_proxy():
    """
    获取随机可用代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()

@app.route('/count')    # 定义接口：获取数量页
def get_counts():
    """
    获取代理池总量
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())


if __name__== '__main__':
    app.run()
# 运行后，Flask会启动一个Web服务，只需要访问对应的接口即可获取到可用代理


# 调度模块：调用以上所定义的3个模块，将3个模块通过多进程的形式运行起来
TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True   # 3个常量均为布尔类型，测试模块
GETTER_ENABLED = True   # 获取模块
API_ENABLED = True  # 接口模块的开关，都为True，则代表模块开启

from multiprocessing import Process
from api import app
from getter import Getter
from tester import Tester

class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):  # schedule_tester方法用来调度测试模块
        """
        定时测试代理
        """
        tester = Tester()   # 声明一个Tester对象
        while True: # 进入死循环不断调用run方法
            print('测试器开始运行')
            tester.run()    # 只需调用Scheduler的run方法即可启动整个代理池
            time.sleep(cycle)   # 执行完一轮就休眠一段时间，休眠结束后重新再执行

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)

    def run(self):  # run方法是启动入口，分别判断3个模块的开关
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process =Process(target=self.schedule_tester)    # 开关开启，启动时程序新建一个Process进程，设置启动目标
            tester_process.start()  # 调用start方法运行，3个进程可以并行执行，互不干扰

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

# 打开浏览器，当前配置运行在5555端口，打开http://127.0.0.1:5555，即可看到首页
# 再访问http://127.0.0.1:5555/random，即可获取随机可用代理
# 只需要访问此接口即可获取一个随机可用代理：
import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
# 即可获取一个随机代理，是字符串类型，可按照requests使用方法设置
import requests

proxy = get_proxy()
proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy,
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
# 代码地址：https://github.com/Python3WebSpider/ProxyPool
