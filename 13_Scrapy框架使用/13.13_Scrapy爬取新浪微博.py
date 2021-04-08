# 以反爬比较强的网站新浪微博为例，实现Scrapy的大规模爬取
# 1.目标：抓取新浪微博用户的公开基本信息，如用户昵称、头像、用户的关注、粉丝列表以及发布的微博等，抓取后保存至MongoDB

# 2.准备：代理池、Cookies池已经实现并可以正常运行，安装Scrapy、PyMongo库

# 3.爬取思路：要实现用户的大规模爬取，采用的爬取方式是：以微博的几个大V为起点，爬取他们各自的粉丝和关注列表，然后获取粉丝和关注
# 列表的粉丝和关注列表，以此类推，这样下去就可以实现递归爬取。如果一个用户与其他用户有社交网络上的关联，他们的信息就会被爬虫
# 抓取到，这样就可以做到对所有用户的爬取。通过这种方式，可以得到用户的唯一ID，再根据ID获取每个用户发布的微博即可

# 4.爬取分析：选取的爬取站点是：https://m.weibo.cn，此站点是微博移动端的站点。打开该站点会跳转到登录页面，因为主页做了登录限制
# 不过可以直接打开某个用户详情页面，可以在页面最上方看到他的关注和粉丝数量，点击关注，进入到他的关注列表
# F12，切换到XHR过滤器，一直下拉关注列表，即可看到下方会出现很多Ajax请求，这些请求就是获取关注列表的Ajax请求。
# 打开第一个Ajax请求，链接为：https://m.weibo.cn/api/container/getIndex?containerid=231....,
# 请求类型是GET类型，返回结果是JSON格式，将其展开后即可看到其关注的用户基本信息，只需构造这个请求的参数。
# 此链接一共有7个参数：containerid、luicode、lfid、featurecode、type、value、page；
# 最主要的参数就是containerid和page，有了这两个参数，可以获取请求结果。
# 将接口精简为：https://m.weibo.cn/api/container/getIndex?containerid=231051-_followers-_196655407&page=2，这里的
# container_id前半部分是固定的，后半部分是用户的id。这里参数构造出来了，只需修改container_id最后的id和page参数即可获取
# 分页形式的关注列表信息。
# 利用同样的方法，也可以分析用户详情的Ajax链接、用户微博列表的Ajax链接：
# 用户详情API：
user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
# 关注列表API：
follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231-51_-_followers_-_{uid}&page={page}'
# 粉丝列表API：
fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}'
# 微博列表API
weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'
# 此处uid和page分别代表用户ID和分页页码，此API随着时间的变或者微博的改变而变化，以实测为准
# 从几个大V开始抓取，抓取他们的粉丝、关注列表、微博信息、然后递归抓取他们的粉丝和关注列表的粉丝、关注列表、微博信息、递归抓取，
# 最后保存微博用户的基本信息、关注和粉丝列表、发布的微博

# 5.新建项目：用Scrapy实现抓取过程，首先创建一个项目，命令：
scrapy startproject weibo
# 进入项目中，新建一个Spider，名为weibocn，命令：
scrapy genspider weibocn m.weibo.cn
# 首先修改Spider，配置各个Ajax的URL，选取几个大V，将他们的ID赋值成一个列表，实现start_requests方法，也就是一次抓取各个大V的
# 个人详情，然后用parse_user进行解析：
from scrapy import Request, Spider

class WeiboSpider(Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231-51_-_followers_-_{uid}&page={page}'
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'
    start_users = ['3217179555', '1742566624', '2282991915', '1288739185', '3952070245', '5878659096']

    def  start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        self.logger.debug(response)

# 6.创建Item：解析用户的基本信息并生成Item，先定义几个Item，如用户、用户关系、微博的Item：
from scrapy import Item, Field

class UserItem(Item):
    collection = 'users'    # 定义了collection字段，指明保存的Collection名称
    id = Field()
    name = Field()
    avatar = Field()
    cover = Field()
    gender = Field()
    description = Field()
    fans_count = Field()
    follows_count = Field()
    weibos_count = Field()
    verified = Field()
    verified_reason = Field()
    verified_type = Field()
    follows = Field()
    fans = Field()
    crawled_at = Field()

class UserRelationItem(Item):   # 用户的关注和粉丝列表直接定义为一个单独的UserRelationItem
    collection = 'users'    # 并不意味着会将关注和粉丝列表存到一个单独的Collection里，Item和collection不是完全对应的
    id = Field()    # id就是用户的ID
    follows = Field()   # follows就是用户关注列表
    fans = Field()  # fans是粉丝列表

class WeiboItem(Item):
    collection = 'weibo'    #
    id = Field()
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()
    picture = Field()
    pictures = Field()
    source = Field()
    text = Field()
    raw_text = Field()
    thumbnail = Field()
    user = Field()
    created_at = Field()
    crawled_at = Field()

# 7.提取数据：开始解析用户的基本信息，实现parse_user方法：
def parse_user(self, response): # 一共完成了两个操作
    """
    解析用户信息
    :param self: Response对象
    """
    result = json.loads(response.text)  # 解析JSON提取用户信息
    if result.get('data').get('userInfo'):
        user_info = result.get('data').get('userInfo')
        user_item = UserItem()
        field_map = {   # 并没有采用常规的逐个赋值方法，而是定义一个字段映射关系。可能和JSON中用户的字段名称不同
            'id ': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
            'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
            'follows_count': 'follow_count', 'weibos_count': 'statues_count', 'verified': 'verified',
            'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
        }   # 所以在这里定义成一个字典
        for field, attr in field_map.items():   # 然后遍历字典的每个字段实现逐个字段的赋值
            user_item[field] = user_info.get(attr)
            yield  user_item    # 并生成UserItem返回
            # 关注
            uid = user_info.get('id')   # 构造用户的关注、粉丝、微博的第一页的链接，并生成Request，
            yield Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follows, # 需要的参数只有用户ID
                          meta={'page': 1, 'uid': uid}) # 初始页码设置为1即可
            # 粉丝
            yield Request(self.fan_url.format(uid=uid, page=1), callback=self.parse_fans,
                          meta={'page': 1, 'uid': uid})
            # 微博
            yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
                          meta={'page': 1, 'uid': uid})
# 接下来，还需要保存用户的关注和粉丝列表，以关注列表为例，解析方法为parse_follows：
def parse_follows(self, response):  # 这个方法里做了三件事
    """
    解析用户关注
    :param response: Response对象
    """
    result = json.loads(response.text)  # 解析关注列表中的每个用户信息并发起新的解析请求
    if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards'))
        and result.get('data').get('cards')[-1].get('card_group'):
        # 解析用户
        follows = result.get('data').get('cards')[-1].get('card_group')
        for follow in follows:
            if follow.get('usr'):
                uid = follow.get('user').get('id')  # 首先解析关注列表的信息，得到用户的ID，
                yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
                # 然后再利用user_url构造访问用户详情的Request
        # 关注列表
        uid = response.meta.get('uid')  # 提取用户关注列内的关键信息并生成UserRelationItem
        user_relation_item = UserRelationItem() # 就建立了一个存有用户ID和用户部分关注列表的UserRelationItem
        follows = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')}
                   for follow in follows]   # id字段直接设置成用户的ID，JSON返回数据中的用户信息有很多冗余子弹
        user_relation_item['id'] = uid  # 只提取关注用的ID和用户名
        user_relation_item['follows'] = follows # 然后赋值给follows字段，
        user_relation_item['fans'] = [] # fans字段设置成空列表
        yield user_relation_item    # 合并且保存具有同一个ID的UserRelationItem的关注和粉丝列表
        # 下一页关注
        page = response.meta.get('page') + 1    # 提取下一页关注，将此请求的分页页码加1即可，分页页码通过Request的meta属性
        yield Request(self.follow_url.format(uid=uid, page=page), callback=self.parse_follows,
                      meta={'page':page, 'uid': uid})   # 进行传递，Response的meta来接收，构造并返回下一页的Request
# 抓取粉丝列表的原理和抓取关注列表原理相同，略

# 抓取用户的微博信息parse_weibos：
def parse_weibos(self, response):   # 完成了两件事
    """
    解析微博列表
    :param response: Response对象
    """
    result = json.loads(response.text)  # 提取用户的微博信息
    if result.get('ok') and result.get('data').get('cards'):
        weibos = result.get('data').get('cards')
        for weibo in weibos:
            mblog = weibo.get('mblog')
            if mblog:
                weibo_item = WeiboItem()
                field_map = {   # 建立了一个字段映射表，实现批量字段赋值
                    'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                        'created_at': 'created_at', 'reposts_count': 'reposts_count', 'picture': 'original_pic',
                        'pictures': 'pics', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
                        'thumbnail': 'thumbnail_pic'
                }
                for field, attr in field_map.items():
                    weibo_item[field] = mblog.get(attr)
                    weibo_item['user'] = response.meta.get('uid')
                    yield weibo_item    # 生成WeiboItem
                # 下一页微博
                uid = response.meta.get('uid')  # 提取下一页的微博列表，同样需要传入用户ID和分页页码
                page = response.meta.get('page') + 1
                yield Request(self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibos,
                              meta={'uid': uid, 'page': page})
# 微博的Spider已经完成

# 8.数据清洗：有些微博不是标准时间，可能显示刚刚、几分钟前、几小时前、昨天等，需统一转化这些时间，实现一个parse_time方法：
def parse_time(self, date): # 用正则来提供一些关键数字，用time库来实现标准时间的转换
    if re.match('刚刚', date):
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    if re.match('\d+分钟前', date):    # 爬取的时间会赋值为created_at字段，用正则匹配此时间，表达式写作\d+分钟前，
        minute = re.match('(\d+)', date).group(1)   # 如果提取到的时间符合这个表达式，就提取其中的数字，就可获取分钟数了
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.teim() - float(minute) * 60))
        # 使用time模块的strftime方法，第一个参数传入要转换的时间格式，第二个参数就是事件戳，当前时间戳-此分钟数*60=当时时间戳
    if re.match('\d+小时前', date):
        hour = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
    if re.match('昨天.*', date):
        date = re.match('昨天(.*)', date).group(1).strip()
        date = time.strftime('%Y-%m-%d', time.localtime() - 24 * 60 * 60) + ' ' + date
    if re.match('\d{2}-\d{2}', date):
        date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
    return date

# Pipeline实现处理：
class WeiboPipeline():
    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            if item.get('created_at'):
                item['created_at'] = item['created_at'].strip()
                item['created_at'] = self.parse_time(item.get('created_at'))
# 在Spider里没有对crawled_at字段赋值，代表爬取时间，可以统一将其赋值为当前时间，实现：
class TimePipeline():
    def process_item(self, item, spider):
        if isinstance(item, UserItem) or isinstance(item, WeiboItem):   # 判断item如果是UserItem或WeiboItem类型，
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime()) # 那就给他的crawled_at字段赋值为当前时间
            item['crawled_at'] = now
        return item
# 通过两个Pipeline，完成了数据清洗工作，这里主要是时间的转换

# 9.数据存储：实现MongoPipeline类：
import pymongo

class MongoPipeline(object):    # 当前MongoPipeline和前面所写有所不同
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[UserItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[WeiboItem.collection].create_index([('id', pymongo.ASCENDING)])

    def open_spider(self, spider):  # open_spider里添加了Collection索引，大规模爬取，爬取过程涉及数据的更新问题
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[UserItem.collection].create_index([('id', pymongo.ASCENDING)])# 为两个Item都添加了索引，索引的字段是id
        self.db[WeiboItem.collection].create_index([('id', pymongo.ASCENDING)]) # 为每个Collection建立索引，大提高检索效率

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):   # process_item方法存储使用的update方法，第一参数是查询条件，第二个是爬取的Item
        # 第三个参数设置为True，数据不存在，则插入数据。就可以做到数据存在即更新、数据不存在即插入，从而获得去重的效果
        if isinstance(item, UserItem) or isinstance(item, WeiboItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)   # 使用$set符，爬取到重复的数据
            # 即可对数据进行更新，同时不会删除已存在的字段，
            # 如不加$set操作符，会直接进行item替换，会导致已存在的字段加关注和粉丝列表清空
        if isinstance(item, UserRelationItem):
            self.db[item.collection].update(
                {'id': item.get('id')},
                {'$addToSet':   # 对于用户的关注和粉丝列表，使用一个新的操作符$addToSet，可以向列表类型的字段插入数据同时去重
                     {  # 值就是需要操作的字段名称。
                         'follows': {'$each': item['follows']}, # 利用$each操作符对需要插入的列表数据进行了遍历
                         'fans': {'$each': item['fans']}    # 以逐条插入用户的关注或粉丝数据到指定的字段
                     }
                }, True)
        return item

# 10.Cookies池对接：需要做一些防范反爬虫的措施才可以顺利完成数据爬取
# 如果没有登录而直接请求微博的API接口，非常容易导致403转态码，在这里我们实现一个Middleware，为每个Request添加随机的Cookies
# 先开启Cookies池，使API模块正常运行，如在本地运行5000端口，访问http://localhost:5000/weibo/random,即可获取随机的Cookies，
# 也可以将Cookies池部署到远程的服务器，只需改变更改访问的链接
# 在本地启动Cookies池，实现一个Middleware：
class CookiesMiddleware():  # 启用了该Middleware
    def __init__(self, cookies_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_url = cookies_url

    def get_random_cookies(self):   # 每个请求都会被赋值随机的Cookies，即可模拟登录后的请求，403状态码基本都不会出现
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider): # 给request对象的cookies属性赋值，
        self.logger.debug('正在获取Cookies')    # 获取的随机Cookies，就成功得为每一次请求赋值Cookies了
        cookies = self.get_random_cookies() # 请求此Cookies池接口并获取接口返回的随机Cookies
        if cookies:
            request.cookies = cookies   # 获取成功，返回Cookies
            self.logger.debug('使用Cookies ' + json.dumps(cookies))   # 返回False

    @classmethod
    def from_crawler(cls, crawler): # 首先利用from_crawler方法获取COOKIES_URL变量
        settings = crawler.settings # 定义在settings.py里，就是刚才我们所说的接口。
        return cls(
            cookies_url=settings.get('COOKIES_URL')
        )

# 11.代理池对接：微博还有一个反爬措施：检测到同一IP请求过大时就会出现414状态码。
# 如果遇到这样的情况可以切换代理。如，在本地5555端口运行，获取随机可用代理的地址为：http://localhost:5555/random,访问此接口
# 即可获取一个随机可用代理。再实现一个Middleware：
class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self): # 请求代理池的接口获取随机代理
        try:
            response = request.get(self.proxy_url)
            if response.status_code == 200: # 如获取成功，返回该代理
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False    # 否则返回False

    def process_request(self, request, spider): # 我们给request对象的meta属性赋值一个proxy字段，该字段的值就是代理
        if request.meta.get('retry_times'): # 赋值代理的判断条件是当前retry_times不为空，就是说第一次请求失败后才启用代理，
            proxy = self.get_random_proxy() # 因为使用代理后访问速度会慢一点
            if proxy:   # 我们在这里设置了只有重试的时候才启用代理，否则直接请求，
                uri = 'https://{proxy}'.format(proxy=proxy) # 可以保证在没有被封禁的情况下直接爬取，保证了爬取速度
                self.logger.debug('使用代理 ' + proxy)
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )

# 12.启用Middleware:在配置文件中启用这两个Middleware，修改settings.py：
DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.CookiesMiddleware': 554,
    'weibo.middlewares.ProxyMiddleware': 555,
}
# 优先级设置，Scrapy的默认Downloader Middleware设置：
{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
}
# 要使自定义的CookiesMiddleware生效，在内置的CookiesMiddleware之前调用。内置的CookiesMiddleware的优先级为700，设置一个小于
# 700的数字即可
# 要使得自定义的ProxyMiddleware生效，在内置的HTTPProxyMiddleware前调用。内置的HTTPProxyMiddleware的优先级为750，设置一个小于
# 750的数字即可

# 13.运行：运行命令启动爬虫：
scrapy crawl weibocn

# 14.代码地址：https://github.com/Python3WebSpider/Weibo
