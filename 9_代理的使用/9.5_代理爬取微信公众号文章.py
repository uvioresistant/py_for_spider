# 1.利用代理爬取微信公众号文章，提取正文、发表日期、公众号等内容，爬取来源是搜狗微信，链接http://weixin.sogou.com，保存到MySQL
# 2.需要用的Python库：aiohttp、requests、redis-py、pyquery、Flask、PyMySQL
# 3.爬取分析
# 搜索后，结果的URL中有很多无关GET请求参数，将无关的参数去掉，保留type和query参数
# http://weixin.sougou.com/weixin?type=2&query=NBA，关键字为NBA，类型为2,2代表搜索微信文章
# 如果没有输入账号登录，只能看到10页的内容，登录后可以看到100页，爬取更多内容，需要登录并使用Cookies爬取
# 搜狗微信反爬虫能力强，连续刷新，会弹出验证302，选择识别验证码并解封，也可以使用代理直接切换IP
# 代理使用代理池，还需要更改检测的URL为搜狗微信站点
# 对于反爬能力强的网站来说，遇到返回状态就需要重试，故采用另一种爬取方式，借助数据库构造一个爬取队列，待爬取请求都放到队列里，
# 失败了重新放回队列，会被重新调度爬取。采用Redis队列数据结构，新请求加入队列，需要重试的请求也放回队列。调度时队列不为空，
# 就把一个个请求取出执行，得到响应后进行解析，提取出想要的结果。
# 采用MySQL存储，借助PyMySQL库，将爬取结果构造为字典，实现动态存储

# 4.构造请求：实现Request的数据结构，需要包含必要信息，请求链接、请求头、请求方式、超时时间。需要实现对应的方法来处理响应，
# 需要再加一个Callback回调函数。翻页请求需要代理来实现，还需要参数NeedProxy。请求失败次数太多，不再请求，需要加失败次数的记录
# 字段都需要作为Request的一部分，组成完整的Request对象放入队列调度，从队列获取出的时候直接执行Request对象即可
# 采用继承requests库中的Request对象来实现，将请求Request作为整体对象去执行，得到响应后再返回，requests库的get、post方法
# 都是通过执行Request对象实现的。

# 需要继承Request对象重新实现一个请求，定义为WeixinRequest
TIMEOUT = 10
from requests import Request

class WeixinRequest(Request):
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method, url, headers)
        self.callback = callback    # 加入额外参数callback回调函数：知道请求的响应用什么方法来处理
        self.need_proxy = need_proxy    # 是否需要代理爬取
        self.fail_time = fail_time      # 失败次数：可以知道请求失败了多少次，判断失败次数是否到了阈值，该不该丢弃这个请求
        self.timeout = timeout      # 超时时间

# 5.实现请求队列：构造请求队列，实现请求的存取，一个放，一个取，利用Redis的rpush和lpop方法
# 存取不能直接存Request对象，Redis存的是字符串，在存Request对象前先把它序列化，取出来是再反序列化，过程可用pickle模块实现
from pickle import dumps, loads
from request import WeixinRequest
class RedisQueue():
    def __init__(self):
        """
        初始化Redis
        """
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def add(self, request):
        """
        向队列添加序列化后的Request
        :param request: 请求对象
        :param fail_time:失败次数
        :return: 添加结果
        """
        if isinstance(request, WeixinRequest):  # 判断Request的类型，如果是WeixinRequest，
            return self.db.rpush(Redis_KEY, dumps(request)) # 程序会用pickle的dumps方法序列化，再调用rpush方法加入队列
        return False

    def pop(self):
        """
        取出下一个Request并反序列化
        :return: Request or None
        """
        if self.db.llen(REDIS_KEY): # 调用lpop方法将请求从队列取出，
            return loads(self.db.lpop(REDIS_KEY))   # 再用pickle的loads方法将其转为WeixinRequest对象
        else:
            return False

    def empty(self):    # empty方法返回队列是否为空，只需判断队列长队是否为0即可
        return self.db.llen(REDIS_KEY) == 0


# 6.修改代理池：将代理池检测的URL修改成收购微信站点，以便把被搜狗微信站点封禁的代理剔除掉，留下可用代理
# 将代理池的设置文件中的TEST_URL修改一下，被封的代理就会减分，正常请求的代理就赋值100，留下的就是可用代理
# 修改后将获取模块、检测模块、接口模块的开关都设置为True，运行代理池，数据库留下的100分代理就是针对搜狗微信的可用代理了
# 同时访问代理接口，设置为5555，访问http：//127.0.0.1:5555/random，可获取到随机可用代理
# 定义一个函数来获取随机代理：
PROXY_POOL_URL = 'http://127.0.0.1:5555/random'
def get_proxy(self):
    """
    从代理池获取代理
    :return:
    """
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            print('Get Proxy', response.text)
            return response.text
        return None
    except requests.ConnectionError:
        return None


# 7.第一个请求，构造第一个请求放到队列里供调度。定义Spider类，实现start方法
from requests import Session
from db import RedisQueue
from request import WeixiinRequest
from urllib.parse import urlencode


class Spider():     # 定义Spider类
    base_url = 'http://weixin.sogou.com/weixin' # 设置全局变量
    keyword = 'NBA'
    headers = {     # 请求头，浏览器登录账号，开发者工具里将请求头复制出来，带上Cookie字段，才能爬取100页内容
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh=TW;q=0.2,mt;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'IPLOC=CN1100; SUID=6FEDCF3C541C970A000000005968CF55; SUV=1500041046435211;'
          'ABTEST=0|1500041048|v1; SNUID=CEA85AE02A2F7E6EAFF9C1FE2ABEBE6F; weixinIndexVisited=1;'
          'JSESSIONID=aaar_m7LEIW-jg_gikPZv; Id=WKllllllll2BzGMVlllllV0o8cUlllll5G@HbZllll9lllllRklll5'
                  '@@@@@@@@@@',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_12_3)AppleWebKit/537.36(KHTML, likeGecko)'
          'Chrome/59.0.3071.115 Safari/537.36'
    }
    session = Session() # 初始化Session，执行请求
    queue = RedisQueue()    # 初始化RedisQueue对象，存储请求

    def start(self):
        """
        初始化工作
        :return:
        """
        # 全局更新Headers，使得所有请求都能应用Cookies
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + urlencode({'query': self.keyword, 'type': 2})
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True)#改URL构造WeixinRequest
        # 回调函数是Spider类的的parse_index方法，当请求成功后，用parse_index来处理和解析，need_proxy参数设置为True，需要代理
        # 调度第一个请求
        self.queue.add(weixin_request)  # 调用RedisQueue的add方法，将请求加入队列，等待调度


# 8.调度请求：加入第一个请求后，开始调度，从队列中取出请求，将结果解析出来，生成新请求加入队列，拿出新请求，解析结果，生成
# 新请求加入队列，循环往复执行，直到队列中没有请求，代理爬取结束
VALID_STATUSES = [200]

def schedule(self):     # 实现schedule方法，内部是一个循环，循环的判断是队列不为空
    """
    调度请求
    :return:
    """
    while not self.queue.empty():       # 当队列不为空时，
        weixin_request = self.queue.pop()       # 调用pop方法取出下一个请求
        callback =weixin_request.callback
        print('Schedule', weixin_request.url)
        response = self.request(weixin_request)     # 调用request方法执行这个请求
        if response and response.status_code in VALID_STATUSES:
            results = list(callback(response))
            if results:
                for result in results:  # schedule方法将返回结果进行遍历
                    print('New Result', result)
                    if isinstance(result, WeixinRequest):   # 利用isinstance方法判断返回结果，结果是WeixinRequest，重新加入
                        self.queue.add(result)
                    if isinstance(result, dict):
                        self.mysql.insert('articles', result)
            else:
                self.error(weixin_request)
        else:
            self.error(weixin_request)

# request方法实现：
from requests import ReadTimeout, ConnectionError

def request(self, weixin_request):
    """
    执行请求
    :param weixin_request: 请求
    :return: 响应
    """
    try:
        if weixin_request.need_proxy:
            proxy = get_proxy()     # 判断请求是否需要代理，如果需要，调用get_proxy方法获取代理，
            if proxy:   #
                proxies = {
                    'http': 'http://' + proxy,
                    'https': 'https://' + proxy
                }
                return self.session.send(weixin_request.prepare(),  # 调用Session的send方法执行请求，请求调用了prepare方法
                                         # 转化为Prepared Request
                     timeout=weixin_request.timeout, allow_redirects=False, proxies=proxies)
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False)
                    # 同事设置allow_redirects为False，timeout是该请求的超时时间，最后响应返回。
    except (ConnectionError, ReadTimeout) as e:
        print(e.args)
        return False
# request方法执行后，得到False，请求失败，连接错误，或Response对象，还需要判断状态码，如果和发，解析，否则重新将请求加回队列

# 状态码合法，解析是调用WeixinRequest的回调函数进行解析，如回调函数是parse_index：
from pyquery import PyQuery as pq

def parse_index(self, response):
    """
    解析索引页
    :param response: 响应
    :return: 新的响应
    """
    doc = pq(response.text)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        url = item.attr('href')
        weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
        yield  weixin_request
    next = doc('#sogou_next').attr('href')
    if next:
        url = self.base_url + str(next)
        weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)
        yield  weixin_request
# 该方法首先获取本页所有微信文章链接，另一件事获取下一页链接，再构造成WeixinRequest后yield返回
# 第一次循环结束。
# while循环继续执行，队列包含第一页内容的文章详情页请求和下一页的请求，第二次循环得到的下一个请求就是文章详情页的请求，
# 重新调用request方法获取其相应，调用其对应的回调函数解析。此时详情页请求的回调方法不同，是parse_detail方法：
def parse_detail(self, response):
    """
    解析详情页
    :param response:响应
    :return: 微信公众号文章
    """
    doc = pq(response.text)
    data = {
        'title': doc('.rich_media_title').text(),
        'content': doc('.rich_media_content').text(),
        'data': doc('#post-date').text(),
        'nickname': doc('#js_profile_qrcode > div > strong').text(),
        'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    }
    yield data
# 此方法解析了微信文章详情页的内容，提取出它的标题、正文文本、发布日期、发布人昵称、微信公众号名称，将信息组合成一个字典
# 返回后还需要判断类型，字典类型，程序就调用mysql对象的insert方法将数据存入数据库
# 第二次循环执行完毕、三次、四次，解析完毕后返回结果以便存储，直到爬取完毕


# 完善整个Spider代码：
import requests
from requests import Request
from pickle import dumps, loads
from request import WeixinRequest
from requests import Session
from db import RedisQueue
from request import WeixiinRequest
from urllib.parse import urlencode
from requests import ReadTimeout, ConnectionError
from pyquery import PyQuery as pq


class Spider():     # 定义Spider类
    base_url = 'http://weixin.sogou.com/weixin' # 设置全局变量
    keyword = 'NBA'
    headers = {     # 请求头，浏览器登录账号，开发者工具里将请求头复制出来，带上Cookie字段，才能爬取100页内容
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh=TW;q=0.2,mt;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'IPLOC=CN1100; SUID=6FEDCF3C541C970A000000005968CF55; SUV=1500041046435211;'
          'ABTEST=0|1500041048|v1; SNUID=CEA85AE02A2F7E6EAFF9C1FE2ABEBE6F; weixinIndexVisited=1;'
          'JSESSIONID=aaar_m7LEIW-jg_gikPZv; Id=WKllllllll2BzGMVlllllV0o8cUlllll5G@HbZllll9lllllRklll5'
                  '@@@@@@@@@@',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_12_3)AppleWebKit/537.36(KHTML, likeGecko)'
          'Chrome/59.0.3071.115 Safari/537.36'
    }
    session = Session() # 初始化Session，执行请求
    queue = RedisQueue()    # 初始化RedisQueue对象，存储请求
    mysql = MySQL()

    def get_proxy(self):
        """
        从代理池获取代理
        :return:
        """
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                print('Get Proxy', response.text)
                return response.text
            return None
        except requests.ConnectionError:
            return None

    def start(self):
        """
        初始化工作
        :return:
        """
        # 全局更新Headers，使得所有请求都能应用Cookies
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + urlencode({'query': self.keyword, 'type': 2})
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True)#改URL构造WeixinRequest
        # 回调函数是Spider类的的parse_index方法，当请求成功后，用parse_index来处理和解析，need_proxy参数设置为True，需要代理
        # 调度第一个请求
        self.queue.add(weixin_request)  # 调用RedisQueue的add方法，将请求加入队列，等待调度

def parse_index(self, response):
    """
    解析索引页
    :param response: 响应
    :return: 新的响应
    """
    doc = pq(response.text)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        url = item.attr('href')
        weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
        yield  weixin_request
    next = doc('#sogou_next').attr('href')
    if next:
        url = self.base_url + str(next)
        weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)
        yield  weixin_request

def parse_detail(self, response):
    """
    解析详情页
    :param response:响应
    :return: 微信公众号文章
    """
    doc = pq(response.text)
    data = {
        'title': doc('.rich_media_title').text(),
        'content': doc('.rich_media_content').text(),
        'data': doc('#post-date').text(),
        'nickname': doc('#js_profile_qrcode > div > strong').text(),
        'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    }
    yield data

def request(self, weixin_request):
    """
    执行请求
    :param weixin_request: 请求
    :return: 响应
    """
    try:
        if weixin_request.need_proxy:
            proxy = get_proxy()     # 判断请求是否需要代理，如果需要，调用get_proxy方法获取代理，
            if proxy:   #
                proxies = {
                    'http': 'http://' + proxy,
                    'https': 'https://' + proxy
                }
                return self.session.send(weixin_request.prepare(),  # 调用Session的send方法执行请求，请求调用了prepare方法
                                         # 转化为Prepared Request
                     timeout=weixin_request.timeout, allow_redirects=False, proxies=proxies)
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=False)
                    # 同事设置allow_redirects为False，timeout是该请求的超时时间，最后响应返回。
    except (ConnectionError, ReadTimeout) as e:
        print(e.args)
        return False

def error(self, weixin_request):
    """
    错误处理
    :param weixin_request: 请求
    :return:
    """
    weixin_request.fail_time = weixin_request.fail_time + 1
    print('Request Failed', weixin_request.fail_time, 'Times', weixin_request.url)
    if weixin_request.fail_time < MAX_FAILED_TIME:
        self.queue.add(weixin_request)

def schedule(self):     # 实现schedule方法，内部是一个循环，循环的判断是队列不为空
    """
    调度请求
    :return:
    """
    while not self.queue.empty():       # 当队列不为空时，
        weixin_request = self.queue.pop()       # 调用pop方法取出下一个请求
        callback =weixin_request.callback
        print('Schedule', weixin_request.url)
        response = self.request(weixin_request)     # 调用request方法执行这个请求
        if response and response.status_code in VALID_STATUSES:
            results = list(callback(response))
            if results:
                for result in results:  # schedule方法将返回结果进行遍历
                    print('New Result', result)
                    if isinstance(result, WeixinRequest):   # 利用isinstance方法判断返回结果，结果是WeixinRequest，重新加入
                        self.queue.add(result)
                    if isinstance(result, dict):
                        self.mysql.insert('articles', result)
            else:
                self.error(weixin_request)
        else:
            self.error(weixin_request)

def run(self):
    """
    入口
    :return:
    """
    self.start()
    self.schedule()


if __name__ == '__main__':
    spider = Spider()
    spider.run()    # 加了一个run方法作为入口，启动柜时，只需执行Spider的run方法即可

# 9.MySQL存储：存储模块，需要定义一个MySQL类供存储数据
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'foobared'
REDIS_KEY = 'weixin'

import pymysql
from config import *

class MySQL():
    def __init__(self, host=MySQL_HOST, username=MySQL_USER, password=MySQL_PASSWORD, port=MYSQL_PORT,
                 database=MYSQL_DATABASE):
                """
                MySQL初始化
                :param host:
                :param username:
                :param password:
                :param port:
                :param database:
                """
                try:
                    self.db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
                    self.cursor = self.db.cursor()
                except pymysql.MySQLError as e:
                    print(e.args)

    def insert(self, table, data):  # insert方法传入表名和字典即可动态构造SQL，SQL构造之后执行即可插入数据
        """
        插入数据
        :param table:
        :param data:
        :return:
        """
        keys = ', '.json(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql_query = 'insert into %s (%s) values (%s)' % (table, keys, values)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()

CREATE TABLE ~articles~  (
    ~id~ int(11) NOT NULL,
    ~title~ varchar(255) NOT NULL,
    ~content~ text NOT NULL,
    ~date~ varchar(255) NOT NULL,
    ~wechat~ varchar(255) NOT NULL,
    ~nickname~ varchar(255) NOT NULL
)  DEFAULT CHARSET=utf8;
ALTER TABLE ~articles~ ADD PRIMARY KEY (~id~);
# 程序首先调度了第一页结果对应的请求，获取了代理执行此请求，随后得到了11个新请求，请求都是WeixinRequeset类型，将其再加入队列。
# 继续调度新加入的请求，就是文章详情页对应的请求，再执行，得到的就是文章详情对应的提取结果，提取结果是字典类型

# 代码地址：https://github.com/Python3WebSpider/Weixin,运行前先配置好代理池
